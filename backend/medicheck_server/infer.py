"""MediCheck pill verification: the inference module used by the server (POST /v1/pills/verify).

Runs the two ONNX models of the final release on CPU and applies the decision rule that was measured on the
validation fold (MediCheck_decisions.md sec. 0, 4, 12.5):

  1. detector (YOLO26s, NMS inside the ONNX file): Ultralytics letterbox to 640, keep boxes with confidence >= 0.5,
     optionally only boxes whose centre lies inside the capture frame sent by the app;
  2. crop every box with a margin of 13% of its longer side, longest side 512, pad to a gray square of 384,
     ImageNet normalisation;
  3. recognizer (DINOv3 ViT-S/16 + cosine head): cosine to the 107 class prototypes;
  4. every expected pill of the current dose is a slot whose allowed classes come from the drug-name lookup;
     pair score = best cosine over the slot's allowed classes - comp x best cosine over the classes not allowed
     anywhere on the prescription; optimal assignment (scipy linear_sum_assignment);
  5. a pill is green when its pair score >= threshold and its class is measurable (seen in >= 2 prescription
     groups); the dose is green only when the number of pills equals the number of expected pills and every pill
     is green (exactly the scene rule of the evaluation, so the measured safety holds);
  6. a pill that is not green is red when it confidently matches a drug of another dose of the same prescription,
     or a class outside the prescription (red thresholds are UX settings calibrated on val, they never make
     anything green); otherwise yellow ("check the box").

Only numpy / onnxruntime / OpenCV / Pillow / SciPy are needed (no PyTorch).
"""
from __future__ import annotations

import csv, io, json, os, re, time
from dataclasses import dataclass

import cv2
import numpy as np
import onnxruntime as ort
from PIL import Image, ImageFile, ImageOps
from scipy.optimize import linear_sum_assignment

ImageFile.LOAD_TRUNCATED_IMAGES = True
NCLS = 107
GRAY = (128, 128, 128)
_MEAN = np.array([0.485, 0.456, 0.406], np.float32) * 255
_STD = np.array([0.229, 0.224, 0.225], np.float32) * 255
SESSION_VI = {"sang": "sáng", "trua": "trưa", "chieu": "chiều", "toi": "tối"}


def norm_name(s: str) -> str:
    """Drug-name key used by the lookup table: lower case, single spaces."""
    return re.sub(r"\s+", " ", str(s).strip().lower())


@dataclass
class Line:
    """One prescription line as sent by the app."""
    line_id: str
    name: str
    count: int = 1                 # pills of this line in the current dose (session lines only)
    sessions: tuple = ()           # doses of the day where this line is taken (other lines; for the red message)


class PillVerifier:
    def __init__(self, model_dir: str, lookup_csv: str | None = None, threads: int = 4):
        self.cfg = json.load(open(os.path.join(model_dir, "deploy_config.json"), encoding="utf-8"))
        so = ort.SessionOptions(); so.intra_op_num_threads = threads
        prov = ["CPUExecutionProvider"]
        self.det = ort.InferenceSession(os.path.join(model_dir, self.cfg["detector"]["file"]), so, providers=prov)
        self.rec = ort.InferenceSession(os.path.join(model_dir, self.cfg["recognizer"]["file"]), so, providers=prov)
        d, r, k = self.cfg["detector"], self.cfg["recognizer"], self.cfg["decision"]
        self.imgsz, self.conf = int(d["imgsz"]), float(d["conf"])
        self.size, self.margin, self.crop_max = int(r["size"]), float(r["crop_margin"]), int(r["crop_max_side"])
        self.comp, self.thr = float(k["comp"]), float(k["threshold"])
        self.measurable = {int(c) for c in k["measurable_classes"]}
        red = self.cfg.get("red", {})
        self.thr_red_other = float(red.get("other_dose_threshold", self.thr))
        self.thr_red_out = float(red.get("outside_threshold", self.thr))
        q = self.cfg.get("quality", {})
        self.min_brightness = float(q.get("min_brightness", 0.0))
        self.min_sharpness = float(q.get("min_sharpness", 0.0))
        self.max_side = int(self.cfg.get("upload", {}).get("max_side", 2048))
        self.version = self.cfg.get("version", "")
        if lookup_csv is None:  # the lookup shipped with the model = the one used for every measurement (train fold only)
            lookup_csv = os.path.join(model_dir, self.cfg.get("lookup", {}).get("file", "lookup_name_classes.csv"))
        self.lookup = {}
        with open(lookup_csv, encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                self.lookup[norm_name(row["name"])] = {int(c) for c in str(row["classes"]).split()}

    # ------------------------------------------------------------------ image
    def load_image(self, data: bytes) -> Image.Image:
        """Decode, apply the EXIF rotation, downscale to the upload size (the app already does it; this is a guard)."""
        im = ImageOps.exif_transpose(Image.open(io.BytesIO(data))).convert("RGB")
        if max(im.size) > self.max_side:
            im.thumbnail((self.max_side, self.max_side), Image.LANCZOS)
        return im

    def quality(self, im: Image.Image) -> dict:
        """Brightness (mean gray 0-255) and sharpness (variance of the Laplacian at long side 1024)."""
        g = np.asarray(im.convert("L"))
        s = 1024 / max(g.shape)
        if s < 1:
            g = cv2.resize(g, (round(g.shape[1] * s), round(g.shape[0] * s)), interpolation=cv2.INTER_AREA)
        return dict(brightness=float(g.mean()), sharpness=float(cv2.Laplacian(g, cv2.CV_64F).var()))

    # ------------------------------------------------------------------ models
    def detect(self, im: Image.Image, frame=None):
        """Boxes (n, 4) normalised x1 y1 x2 y2 and confidences, Ultralytics letterbox (centre, pad 114)."""
        a = np.asarray(im); h, w = a.shape[:2]; S = self.imgsz
        r = min(S / h, S / w)
        nw, nh = int(round(w * r)), int(round(h * r))
        if (nw, nh) != (w, h):
            a = cv2.resize(a, (nw, nh), interpolation=cv2.INTER_LINEAR)
        dw, dh = (S - nw) / 2, (S - nh) / 2
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        a = cv2.copyMakeBorder(a, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114, 114, 114))
        x = np.ascontiguousarray(a.transpose(2, 0, 1)[None], dtype=np.float32) / 255.0
        o = self.det.run(None, {self.det.get_inputs()[0].name: x})[0][0]
        o = o[o[:, 4] >= self.conf]
        b = o[:, :4].copy()
        b[:, [0, 2]] = ((b[:, [0, 2]] - left) / r).clip(0, w) / w
        b[:, [1, 3]] = ((b[:, [1, 3]] - top) / r).clip(0, h) / h
        conf = o[:, 4].astype(float)
        if frame is not None and len(b):
            cx, cy = (b[:, 0] + b[:, 2]) / 2, (b[:, 1] + b[:, 3]) / 2
            k = (cx >= frame[0]) & (cx <= frame[2]) & (cy >= frame[1]) & (cy <= frame[3])
            b, conf = b[k], conf[k]
        return b, conf

    def crop(self, im: Image.Image, box) -> Image.Image:
        """Box + margin of 13% of the longer side, longest side 512 (same geometry as the evaluated crops)."""
        W, H = im.size
        x1, y1, x2, y2 = box[0] * W, box[1] * H, box[2] * W, box[3] * H
        p = self.margin * max(x2 - x1, y2 - y1)
        c = im.crop((int(max(0, x1 - p)), int(max(0, y1 - p)), int(min(W, x2 + p)), int(min(H, y2 + p))))
        c.thumbnail((self.crop_max, self.crop_max))
        return c

    def cosine(self, crops) -> np.ndarray:
        """Cosine (n, 107) of crop images (PIL) to the class prototypes."""
        if not len(crops):
            return np.zeros((0, NCLS), np.float32)
        x = np.stack([np.asarray(ImageOps.pad(c.convert("RGB"), (self.size, self.size), color=GRAY), dtype=np.float32) for c in crops])
        x = ((x - _MEAN) / _STD).transpose(0, 3, 1, 2)
        out = []
        for i in range(0, len(x), 8):
            out.append(self.rec.run(["cosine"], {"image": np.ascontiguousarray(x[i:i + 8])})[0])
        return np.concatenate(out).astype(np.float32)

    # ------------------------------------------------------------------ decision
    def allowed(self, name: str):
        return self.lookup.get(norm_name(name))

    def decide(self, cos: np.ndarray, session_lines, other_lines=(), unchecked_count: int = 0, session: str = "") -> dict:
        """Decision on the cosine matrix of the detected pills (rows) for one dose.
        session_lines: lines of the current dose (Line, with count). Lines whose name is not in the lookup are
        'reminder only' and count as unchecked pills. other_lines: the other lines of the prescription.
        Returns the per-pill result, missing pills, the dose status and the scene score (the quantity whose
        threshold was calibrated: weakest pair, -inf when the dose cannot be green)."""
        n = len(cos)
        slots, slot_line, unchecked = [], [], int(unchecked_count)
        for ln in session_lines:
            al = self.allowed(ln.name)
            if not al:
                unchecked += ln.count
                continue
            for _ in range(int(ln.count)):
                slots.append(sorted(al)); slot_line.append(ln)
        pres = set()
        for ln in list(session_lines) + list(other_lines):
            pres |= self.allowed(ln.name) or set()
        comp_cls = sorted(set(range(NCLS)) - pres)
        compv = cos[:, comp_cls].max(1) if (len(comp_cls) and n) else np.zeros(n, np.float32)

        A = np.full((n, len(slots)), -9.0); C = np.full((n, len(slots)), -1, dtype=int)
        for j, al in enumerate(slots):
            if n:
                sub = cos[:, al]; A[:, j] = sub.max(1); C[:, j] = np.asarray(al)[sub.argmax(1)]
        if self.comp > 0 and len(slots):
            A = A - self.comp * compv[:, None]
        rows, cols = linear_sum_assignment(-A) if (n and len(slots)) else (np.array([], int), np.array([], int))

        pills = [dict(index=i, status=None, reason=None, line_id=None, name=None, score=None, cls=None) for i in range(n)]
        for i, j in zip(rows, cols):
            s, c = float(A[i, j]), int(C[i, j])
            ln = slot_line[j]
            pills[i].update(line_id=ln.line_id, name=ln.name, score=s, cls=c)
            if s >= self.thr and c in self.measurable:
                pills[i].update(status="green", reason="match")
        matched = set(int(j) for j in cols)
        missing = {}
        for j, ln in enumerate(slot_line):
            if j not in matched:
                missing.setdefault(ln.line_id, dict(line_id=ln.line_id, name=ln.name, count=0))["count"] += 1

        # red / yellow for every pill that is not green (matched below threshold, or extra)
        sess_allowed = set().union(*[set(s) for s in slots]) if slots else set()
        pres_list = sorted(pres)
        n_extra_yellow = 0
        for p in pills:
            if p["status"] == "green":
                continue
            i = p["index"]
            # raw red scores (kept for calibration): other dose = like a green pair score but against the lines of
            # the other doses (classes shared with this dose excluded); outside = the mirror image of the pair score
            ro, ro_line = float("-inf"), None
            for ln in other_lines:
                al = sorted((self.allowed(ln.name) or set()) - sess_allowed)
                if not al:
                    continue
                k = int(np.argmax(cos[i, al])); so = float(cos[i, al[k]] - self.comp * compv[i])
                if al[k] in self.measurable and so > ro:
                    ro, ro_line = so, ln
            rx = float("-inf")
            if comp_cls and pres_list:
                k = int(np.argmax(cos[i, comp_cls]))
                so = float(cos[i, comp_cls[k]] - self.comp * cos[i, pres_list].max())
                if comp_cls[k] in self.measurable:
                    rx = so
            p.update(red_other_raw=ro, red_out_raw=rx)
            # an extra pill may belong to a reminder-only line of this dose (its classes are unknown, so it looks
            # "outside the prescription"): while such pills are expected, extra pills are never red "not in prescription"
            maybe_unchecked = p["line_id"] is None and n_extra_yellow < unchecked
            best = None
            if ro >= self.thr_red_other:
                best = (ro, "other_dose", ro_line)
            if not maybe_unchecked and rx >= self.thr_red_out and (best is None or rx > best[0]):
                best = (rx, "not_in_prescription", None)
            if best is not None:
                p.update(status="red", reason=best[1], red_score=best[0])
                if best[2] is not None:
                    p.update(other_line_id=best[2].line_id, other_name=best[2].name, other_sessions=list(best[2].sessions))
            elif maybe_unchecked:
                n_extra_yellow += 1
                p.update(status="yellow", reason="not_checkable")   # may be a pill of a reminder-only line
            else:
                p.update(status="yellow", reason="extra" if p["line_id"] is None else "uncertain" if (p["score"] if p["score"] is not None else -9) < self.thr else "unmeasurable_class")

        count_ok = n == len(slots) + unchecked
        all_green = all(p["status"] == "green" for p in pills if p["line_id"] is not None) and len(matched) == len(slots)
        if n == len(slots) and len(slots) and n and all(C[i, j] in self.measurable for i, j in zip(rows, cols)):
            scene_score = float(A[rows, cols].min())
        else:
            scene_score = float("-inf")
        if count_ok and all_green and unchecked == 0 and n > 0:
            status = "green"
        elif count_ok and all_green and unchecked > 0:
            status = "partial"   # every checkable pill is green, the reminder-only pills must be checked by hand
        else:
            status = "not_green"
        return dict(status=status, scene_score=scene_score, pills=pills, missing=list(missing.values()),
                    n_expected=len(slots) + unchecked, n_detected=n, unchecked=unchecked, session=session)

    # ------------------------------------------------------------------ messages
    @staticmethod
    def pill_message(p: dict) -> str:
        if p["status"] == "green":
            return f"Viên này khớp {p['name']}."
        if p["reason"] == "other_dose":
            ss = [SESSION_VI.get(s, s) for s in p.get("other_sessions") or []]
            when = f"thuốc buổi {' và '.join(ss)}" if ss else "thuốc không thuộc cữ này"
            return f"Viên này là {when} ({p['other_name']}). Đừng uống viên này trong cữ này."
        if p["reason"] == "not_in_prescription":
            return "Viên này không khớp thuốc nào trong đơn, hãy kiểm vỏ hộp trước khi uống."
        if p["reason"] == "not_checkable":
            return "App chưa kiểm được thuốc này bằng hình, hãy kiểm theo vỏ hộp."
        return "App chưa xác nhận được viên này, hãy kiểm vỏ hộp."

    @staticmethod
    def summary(res: dict, quality_issue=None) -> str:
        ses = SESSION_VI.get(res.get("session", ""), res.get("session", ""))
        cu = f"cữ {ses}" if ses else "cữ này"
        if res["n_detected"] == 0:
            return "Không thấy viên thuốc nào. Hãy đặt thuốc lên lòng bàn tay, các viên rời nhau, rồi chụp lại."
        if res["status"] == "green":
            return f"Đúng hết. {res['n_detected']} viên khớp {cu}."
        parts = []
        st = [p["status"] for p in res["pills"]]
        if res["status"] == "partial":
            parts.append(f"{st.count('green')} viên khớp {cu}. Có thuốc app chưa kiểm được bằng hình, hãy kiểm theo vỏ hộp.")
        else:
            if st.count("red"):
                parts.append(f"Có {st.count('red')} viên không đúng, hãy bỏ ra.")
            if st.count("yellow"):
                parts.append(f"Có {st.count('yellow')} viên app chưa xác nhận được.")
            for m in res["missing"]:
                parts.append(f"Còn thiếu {m['count']} viên {m['name']}.")
            if not parts:
                parts.append("App chưa xác nhận được cữ này, hãy kiểm vỏ hộp.")
            if quality_issue == "dark":
                parts.append("Ảnh hơi tối, hãy bật đèn rồi chụp lại.")
            elif quality_issue == "blurry":
                parts.append("Ảnh hơi mờ, hãy giữ máy chắc tay rồi chụp lại.")
        return " ".join(parts)

    # ------------------------------------------------------------------ full request
    def verify(self, image_bytes: bytes, session_lines, other_lines=(), unchecked_count: int = 0, session: str = "",
               frame=None) -> dict:
        t0 = time.perf_counter()
        im = self.load_image(image_bytes)
        q = self.quality(im)
        t1 = time.perf_counter()
        boxes, conf = self.detect(im, frame)
        t2 = time.perf_counter()
        cos = self.cosine([self.crop(im, b) for b in boxes])
        t3 = time.perf_counter()
        res = self.decide(cos, session_lines, other_lines, unchecked_count, session)
        issue = "dark" if q["brightness"] < self.min_brightness else "blurry" if q["sharpness"] < self.min_sharpness else None
        # the quality check never turns a green dose yellow: it only explains a non-green result
        pills = []
        for p in res["pills"]:
            i = p["index"]
            pills.append(dict(box=[round(float(v), 4) for v in boxes[i]], detector_conf=round(float(conf[i]), 3),
                              status=p["status"], reason=p["reason"], line_id=p["line_id"] if p["status"] == "green" else p.get("other_line_id"),
                              name=p["name"] if p["status"] == "green" else p.get("other_name"), message=self.pill_message(p)))
        return dict(status=res["status"], summary=self.summary(res, issue), pills=pills, missing=res["missing"],
                    n_expected=res["n_expected"], n_detected=res["n_detected"],
                    quality=dict(ok=issue is None, issue=issue, **{k: round(v, 1) for k, v in q.items()}),
                    timing_ms=dict(decode=round((t1 - t0) * 1000), detect=round((t2 - t1) * 1000),
                                   recognize=round((t3 - t2) * 1000), total=round((time.perf_counter() - t0) * 1000)),
                    model_version=self.version)
