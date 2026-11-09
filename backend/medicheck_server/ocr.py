"""MediCheck prescription reading (POST /v1/prescriptions/parse): ONNX only, CPU.

  1. text detection  PP-OCRv5 mobile det (det.onnx): long side 960 (multiple of 128), DB post-processing as in PaddleOCR
                     (threshold 0.3, box score 0.6, unclip 1.5); a tilted photo is straightened from the angle of the
                     detected text boxes and detected again;
  2. text recognition VietOCR vgg_transformer (rec_encoder.onnx + rec_decoder.onnx): line image at height 32, greedy
                     decoding (same output as vietocr.Predictor);
  3. layout          text boxes grouped into rows by their vertical centre;
  4. parser          rules for the two VAIPE prescription layouts: drug line "N) NAME ... SL: q", schedule
                     "Sáng/Trưa/Chiều/Tối n", note "trước/sau khi ăn", "khi đau/khi cần" (as-needed), "1/2" (half pill),
                     issue date "Ngày dd/mm/yyyy" or "Ngày dd tháng mm năm yyyy", diagnosis "Chẩn đoán: ..." (display only);
  5. dictionary      the OCR name is matched (accent-insensitive similarity) to the drug-name lookup of the pill models,
                     so a confirmed name is directly usable by POST /v1/pills/verify. Unmatched names stay as read and
                     become "reminder only" in the app. Every result goes through the confirmation screen of the app.
"""
from __future__ import annotations

import difflib, io, json, math, os, re, time, unicodedata

import cv2
import numpy as np
import onnxruntime as ort
import pyclipper
from PIL import Image, ImageOps
from shapely.geometry import Polygon

SESSIONS = ("sang", "trua", "chieu", "toi")


def fold(s: str) -> str:
    """Lower case, no diacritics, single spaces (for matching only)."""
    s = unicodedata.normalize("NFC", str(s)).lower().replace("đ", "d")
    s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", s).strip()


# ------------------------------------------------------------------ detection
class TextDetector:
    def __init__(self, path, so, resize_long=960, thresh=0.3, box_thresh=0.6, unclip_ratio=1.5, max_candidates=1000):
        self.s = ort.InferenceSession(path, so, providers=["CPUExecutionProvider"])
        self.inp = self.s.get_inputs()[0].name
        self.resize_long, self.thresh, self.box_thresh, self.unclip_ratio, self.maxc = resize_long, thresh, box_thresh, unclip_ratio, max_candidates

    def __call__(self, bgr: np.ndarray):
        # = PaddleX DetResizeForTest type 0, limit_type "max": shrink only when the long side exceeds 960, then round
        #   each side to a multiple of 32
        h, w = bgr.shape[:2]
        r = self.resize_long / max(h, w) if max(h, w) > self.resize_long else 1.0
        rh, rw = max(int(round(int(h * r) / 32) * 32), 32), max(int(round(int(w * r) / 32) * 32), 32)
        x = (cv2.resize(bgr, (rw, rh)) if (rh, rw) != (h, w) else bgr).astype(np.float32) / 255.0
        x = (x - np.array([0.485, 0.456, 0.406], np.float32)) / np.array([0.229, 0.224, 0.225], np.float32)
        x = np.ascontiguousarray(x.transpose(2, 0, 1)[None])
        pred = self.s.run(None, {self.inp: x})[0][0, 0]
        return self._boxes(pred, pred > self.thresh, w, h)

    @staticmethod
    def _mini_box(contour):
        rect = cv2.minAreaRect(contour)
        pts = sorted(list(cv2.boxPoints(rect)), key=lambda p: p[0])
        i1, i4 = (0, 1) if pts[1][1] > pts[0][1] else (1, 0)
        i2, i3 = (2, 3) if pts[3][1] > pts[2][1] else (3, 2)
        return np.array([pts[i1], pts[i2], pts[i3], pts[i4]]), min(rect[1])

    @staticmethod
    def _score(pred, box):
        h, w = pred.shape
        xmin, xmax = int(np.clip(np.floor(box[:, 0].min()), 0, w - 1)), int(np.clip(np.ceil(box[:, 0].max()), 0, w - 1))
        ymin, ymax = int(np.clip(np.floor(box[:, 1].min()), 0, h - 1)), int(np.clip(np.ceil(box[:, 1].max()), 0, h - 1))
        mask = np.zeros((ymax - ymin + 1, xmax - xmin + 1), dtype=np.uint8)
        b = box.copy(); b[:, 0] -= xmin; b[:, 1] -= ymin
        cv2.fillPoly(mask, b.reshape(1, -1, 2).astype(np.int32), 1)
        return cv2.mean(pred[ymin:ymax + 1, xmin:xmax + 1], mask)[0]

    def _unclip(self, box):
        poly = Polygon(box)
        d = poly.area * self.unclip_ratio / poly.length
        off = pyclipper.PyclipperOffset(); off.AddPath(box.astype(np.int64).tolist(), pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)
        return np.array(off.Execute(d))

    def _boxes(self, pred, bitmap, dw, dh):
        h, w = bitmap.shape
        cs, _ = cv2.findContours((bitmap * 255).astype(np.uint8), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        out = []
        for c in cs[:self.maxc]:
            pts, s = self._mini_box(c)
            if s < 3 or self._score(pred, pts.reshape(-1, 2)) < self.box_thresh:
                continue
            u = self._unclip(pts)
            if len(u) != 1:
                continue
            box, s = self._mini_box(u.reshape(-1, 1, 2).astype(np.float32))
            if s < 5:
                continue
            box[:, 0] = np.clip(np.round(box[:, 0] / w * dw), 0, dw)
            box[:, 1] = np.clip(np.round(box[:, 1] / h * dh), 0, dh)
            out.append(box.astype(np.float32))
        return out


# ------------------------------------------------------------------ recognition
class TextRecognizer:
    def __init__(self, folder, so=None):
        so = so or ort.SessionOptions()
        self.enc = ort.InferenceSession(os.path.join(folder, "rec_encoder.onnx"), so, providers=["CPUExecutionProvider"])
        self.dec = ort.InferenceSession(os.path.join(folder, "rec_decoder.onnx"), so, providers=["CPUExecutionProvider"])
        v = json.load(open(os.path.join(folder, "rec_vocab.json"), encoding="utf-8"))
        self.chars, self.eos, self.go = v["chars"], v["eos"], v["go"]
        self.h, self.wmin, self.wmax, self.maxlen = v["image_height"], v["image_min_width"], v["image_max_width"], v["max_seq_length"]

    def predict(self, im: Image.Image):
        """Text and mean character probability, exactly like vietocr.Predictor.predict (greedy decoding)."""
        w, h = im.size
        nw = int(self.h * float(w) / float(h)); nw = math.ceil(nw / 10) * 10; nw = min(max(nw, self.wmin), self.wmax)
        x = (np.asarray(im.convert("RGB").resize((nw, self.h), Image.LANCZOS)).transpose(2, 0, 1) / 255.0)[None].astype(np.float32)
        mem = self.enc.run(None, {"image": x})[0]
        toks, probs = [self.go], []
        for _ in range(self.maxlen + 1):
            lg = self.dec.run(None, {"tgt": np.array(toks, np.int64)[:, None], "memory": mem})[0][0, -1]
            p = np.exp(lg - lg.max()); p /= p.sum()
            k = int(p.argmax()); toks.append(k); probs.append(float(p[k]))
            if k == self.eos:
                break
        ids = toks[1:]
        end = ids.index(self.eos) if self.eos in ids else len(ids)
        text = "".join(self.chars[i] for i in ids[:end])
        pr = [p for t, p in zip(toks[1:], probs) if t > 3]
        return text, (float(np.mean(pr)) if pr else 0.0)


# ------------------------------------------------------------------ reader
RX_SES = re.compile(r"(sang|sanq|trua|chieu|chiu|chieo|toi)\s*:?\s*(\d+\s*/\s*\d+|\d+(?:[.,]\d+)?)")
SES_FIX = {"sanq": "sang", "chiu": "chieu", "chieo": "chieu"}
RX_ONE = re.compile(r"(?<=\s)[il|](?=\s*v(ien)?\b)")   # OCR reads the digit 1 before "viên" as the letter I or l
RX_QTY = re.compile(r"sl\s*[:;.]?\s*(\d+)")
RX_START = re.compile(r"^\W*(\d{1,2})\s*[\)\]}]\s*(.*)$")
RX_DATE1 = re.compile(r"ngay\s*(\d{1,2})\s*/\s*(\d{1,2})\s*/\s*(\d{4})")
RX_DATE2 = re.compile(r"ngay\s*(\d{1,2})\s*thang\s*(\d{1,2})\s*nam\s*(\d{4})")
STOP = re.compile(r"^(cong khoan|loi dan|ngay hen|benh nhan|y, bac si|bac sy|bs\.|tai kham|kham lai|ten bo|thuoc dieu tri)")


class PrescriptionReader:
    def __init__(self, model_dir: str, lookup_names, threads: int = 4, match_cutoff: float = 0.8):
        so = ort.SessionOptions(); so.intra_op_num_threads = threads
        d = os.path.join(model_dir, "ocr")
        self.det = TextDetector(os.path.join(d, "det.onnx"), so)
        self.rec = TextRecognizer(d, so)
        self.names = sorted(lookup_names)
        self.fnames = [fold(n) for n in self.names]
        self.cutoff = match_cutoff

    # ---- image
    @staticmethod
    def load(data: bytes, filename: str = "") -> Image.Image:
        if data[:4] == b"%PDF" or filename.lower().endswith(".pdf"):
            import pypdfium2 as pdfium
            page = pdfium.PdfDocument(data)[0]
            return page.render(scale=2).to_pil().convert("RGB")
        im = ImageOps.exif_transpose(Image.open(io.BytesIO(data))).convert("RGB")
        if max(im.size) > 2400:
            im.thumbnail((2400, 2400), Image.LANCZOS)
        return im

    def cells(self, im: Image.Image, deskew: bool = True):
        """Detected text boxes with recognised text; the image is straightened first when the text is tilted."""
        bgr = np.asarray(im)[:, :, ::-1].copy()
        boxes = self.det(bgr)
        angle = 0.0
        if deskew and boxes:
            angs = []
            for b in boxes:
                e = b[1] - b[0]
                if np.hypot(*e) > 40:
                    angs.append(math.degrees(math.atan2(e[1], e[0])))
            if angs:
                angle = float(np.median(angs))
            if abs(angle) > 0.4:
                im = im.rotate(angle, expand=True, fillcolor=(255, 255, 255), resample=Image.BICUBIC)
                bgr = np.asarray(im)[:, :, ::-1].copy(); boxes = self.det(bgr)
        out = []
        for b in boxes:
            x0, y0, x1, y1 = b[:, 0].min(), b[:, 1].min(), b[:, 0].max(), b[:, 1].max()
            if x1 - x0 < 8 or y1 - y0 < 6:
                continue
            t, p = self.rec.predict(im.crop((x0 - 2, max(0, y0 - 2), x1 + 2, y1 + 2)))
            if t.strip():
                out.append(dict(x0=float(x0), y0=float(y0), x1=float(x1), y1=float(y1), text=t.strip(), prob=p))
        return out, angle, im.size

    @staticmethod
    def rows(cells):
        """Group text boxes into rows by vertical centre, left to right inside a row."""
        if not cells:
            return []
        hmed = float(np.median([c["y1"] - c["y0"] for c in cells]))
        rows = []
        for c in sorted(cells, key=lambda c: (c["y0"] + c["y1"]) / 2):
            cy = (c["y0"] + c["y1"]) / 2
            if rows and abs(cy - rows[-1]["cy"]) < 0.5 * hmed:
                r = rows[-1]; r["cells"].append(c); r["cy"] = float(np.mean([(z["y0"] + z["y1"]) / 2 for z in r["cells"]]))
            else:
                rows.append(dict(cy=cy, cells=[c]))
        return [sorted(r["cells"], key=lambda c: c["x0"]) for r in rows]

    def match(self, raw: str):
        f = fold(raw)
        best, score = None, 0.0
        for n, fn in zip(self.names, self.fnames):
            s = difflib.SequenceMatcher(None, f, fn).ratio()
            if s > score:
                best, score = n, s
        return (best if score >= self.cutoff else None), score

    def parse(self, rows):
        drugs, diag, date, in_diag = [], [], None, False
        for r in rows:
            texts = [c["text"] for c in r]; line = " ".join(texts); f = fold(line)
            if date is None and "tai kham" not in f and "hen kham" not in f:
                m = RX_DATE1.search(f) or RX_DATE2.search(f)
                if m:
                    dd, mm, yy = map(int, m.groups())
                    if 1 <= dd <= 31 and 1 <= mm <= 12:
                        date = f"{yy:04d}-{mm:02d}-{dd:02d}"
            m0 = RX_START.match(texts[0]) if texts else None
            if m0 is None and texts and not in_diag and not RX_SES.search(f) and not RX_QTY.search(f) and "uong" not in f and not STOP.match(f):
                # the "N)" prefix can be misread on a photographed paper: a row whose text is a catalog name starts a line
                cand = re.sub(r"^[^a-zA-ZÀ-ỹ]+", "", line)
                if len(cand) >= 5 and self.match(cand)[1] >= 0.9:
                    m0 = re.match(r"^()(.*)$", cand)
                    texts = [cand]
            if f.startswith(("chan doan", "chuan doan", "chan đoan")) or (f.startswith("ch") and "doan" in f[:12]):
                in_diag = True; diag.append(line.split(":", 1)[1].strip() if ":" in line else line); continue
            if m0:
                in_diag = False
                name_parts = [m0.group(2)] + texts[1:]
                name = " ".join(t for t in name_parts if not RX_QTY.search(fold(t)))
                name = re.sub(r"(?i)\s*SL\s*[:;.]?.*$", "", name).strip()
                q = RX_QTY.search(f)
                drugs.append(dict(raw_name=name, quantity=int(q.group(1)) if q else None, schedule={}, notes=[], usage_raw=[],
                                  probs=[c["prob"] for c in r]))
                self._usage(drugs[-1], f, line, start=True)
                continue
            if STOP.match(f):
                in_diag = False
                if drugs:
                    drugs[-1]["closed"] = True
                continue
            if in_diag and not drugs:
                diag.append(line); continue
            if drugs and not drugs[-1].get("closed"):
                d = drugs[-1]
                if d["quantity"] is None:
                    q = RX_QTY.search(f)
                    if q:
                        d["quantity"] = int(q.group(1))
                d["probs"] += [c["prob"] for c in r]
                self._usage(d, f, line)
        out = []
        for i, d in enumerate(drugs, 1):
            name, score = self.match(d["raw_name"])
            amounts = list(d["schedule"].values())
            if not d["schedule"]:
                kind = "as_needed" if any(re.search(r"khi (dau|can|sot|ho)", fold(u)) for u in d["usage_raw"]) else "missing_schedule"
            elif any("/" in a for a in amounts):
                kind = "half_pill"
            else:
                kind = "regular"
            conf = float(min(d["probs"])) if d["probs"] else 0.0
            out.append(dict(index=i, raw_name=d["raw_name"], name=name, name_score=round(score, 3), quantity=d["quantity"],
                            schedule=d["schedule"], dose_type=kind, note=", ".join(dict.fromkeys(d["notes"])) or None,
                            usage_text=" | ".join(d["usage_raw"]) or None, ocr_confidence=round(conf, 3),
                            needs_review=bool(name is None or score < 0.9 or conf < 0.8 or d["quantity"] is None or kind != "regular")))
        return out, (" ".join(diag).strip() or None), date

    @staticmethod
    def _usage(d, f, line, start=False):
        ses = RX_SES.findall(RX_ONE.sub("1", f))
        for k, v in ses:
            d["schedule"][SES_FIX.get(k, k)] = re.sub(r"\s", "", v).replace(",", ".")
        for pat, label in ((r"truoc (khi |bua )?an", "trước khi ăn"), (r"sau (khi |bua )?an", "sau khi ăn"),
                           (r"trong (khi |bua )?an", "trong khi ăn"), (r"khi (dau|can|sot|ho)", None)):
            if re.search(pat, f) and label:
                d["notes"].append(label)
        if not start and (ses or "uong" in f or re.search(r"khi (dau|can|sot)", f)):
            d["usage_raw"].append(line)

    def read(self, data: bytes, filename: str = "") -> dict:
        t0 = time.perf_counter()
        im = self.load(data, filename)
        cells, angle, size = self.cells(im)
        rows = self.rows(cells)
        lines, diag, date = self.parse(rows)
        return dict(lines=lines, diagnosis=diag, issued_date=date, n_text_boxes=len(cells), deskew_angle=round(angle, 2),
                    needs_review=any(l["needs_review"] for l in lines) or not lines,
                    timing_ms=round((time.perf_counter() - t0) * 1000))
