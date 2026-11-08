# MediCheck – Tiến độ phần AI

> **Đọc file này đầu tiên khi mở session mới.** File ghi trạng thái hiện tại, việc tiếp theo và cách làm việc. Quyết định kỹ thuật và bằng chứng: `MediCheck_decisions.md`. Tài liệu ôn bảo vệ: `MediCheck_AI_tong_hop.md`.
>
> Cập nhật lần cuối: 2026-11-08 (sau khi chạy test và giao `backend/` cho nhóm app).

Ký hiệu: ✅ xong · 🔄 đang làm · ⏳ chưa làm

---

## 1. Trạng thái hiện tại

| Giai đoạn | Việc | Trạng thái |
|---|---|---|
| A. Thử nghiệm chọn hướng | C1–C9 (local + smoke test), S1–S3 trên Kaggle | ✅ |
| B. Chốt mô hình | Detector D2-B + bộ nhận dạng R3-B seed 1, ngưỡng 0,0529 | ✅ |
| C. Xuất file triển khai | `out/onnx_final/`: `detector.onnx`, `recognizer.onnx`, `deploy_config.json` (khớp PyTorch) | ✅ |
| D. Module suy luận + máy chủ API | `backend/`: module `PillVerifier` + FastAPI `POST /v1/pills/verify` + `API.md`; kiểm trên val qua module: 90,9% báo xanh, 1,19% / 1,79% | ✅ 08/11 |
| E. Test một lần | Chạy test khóa qua module D: **90,2% báo xanh, cận trên 1,09% / 1,31%** → đạt | ✅ 08/11 |
| F. Giao nhóm app | `backend/` + `API.md` (cách chạy, JSON, code Dart, demo Wi-Fi) trên repo | ✅ 08/11 |

**Bản cuối** (chi tiết `MediCheck_decisions.md` mục 0):
- **Detector:** YOLO26s, ngưỡng tin cậy 0,5, nhánh NMS.
- **Bộ nhận dạng:** DINOv3 ViT-S/16 @384, mở toàn bộ + LLRD 0,75, seed 1.
- **Quyết định:** đối thủ 0,5, ngưỡng 0,0529 (fit với mục tiêu cận trên 1,8%), 14 lớp luôn vàng.
- **Test (chạy một lần, số chính thức): 90,2% cữ đúng được báo xanh; cận trên nhận nhầm 1,09% (viên ngoài đơn) / 1,31% (viên lạ) → đạt chuẩn ≤ 2%.**
- **Val:** qua module 90,9% (PyTorch trước đây 89,5%); cận trên 1,19% / 1,79%. Detector đếm đúng 98,7%; nhận dạng đúng trong ứng viên 95,8%.
- **Tốc độ:** CPU ~1 giây cho 4 viên.

---

## 2. Việc tiếp theo

| # | Việc | Ghi chú |
|---|---|---|
| 1 | ✅ Module suy luận + server (`backend/`), kiểm trên val (`MediCheck_decisions.md` mục 13) | |
| 2 | ✅ Test một lần (`MediCheck_decisions.md` mục 14.1) và giao `backend/` cho nhóm app | |
| 3 | Cổng 22/11: kiểm `deploy_config.json`, đo độ trễ trên laptop demo | Không cần train |
| 4 | OCR (23–29/11): chỉnh nghiêng, gom hàng, parser chẩn đoán, đo độ chính xác | |
| 5 | Hỗ trợ nhóm mobile ghép `POST /v1/pills/verify`; thêm OCR `POST /v1/prescriptions/parse` vào server | |
| 6 | Đồng bộ báo cáo `.docx` theo hàng đợi mục 6; thêm hình (ma trận nhầm, ví dụ ca vàng) | |
| 7 | Sau dự án: người dùng tạo lại token Kaggle | |

---

## 3. Cách làm việc và môi trường

- Phụ trách AI lo phần AI và chốt tài liệu; lựa chọn kỹ thuật được quyết theo hướng senior DL/CV, kèm bằng chứng, phản biện nhiều góc, ghi vào `MediCheck_decisions.md`. Chuẩn an toàn ≤ 2% không bao giờ nới.
- Sau mỗi task: cập nhật mọi tài liệu liên quan (decisions, progress, brainstorm nếu là quyết định sản phẩm, tong_hop, `vaipe_analysis.md` khi liên quan) và hàng đợi `.docx` (mục 6).
- **Kaggle:** quota 30 giờ/tuần, **không reset đến 15/11**; còn ~17 giờ (đã dùng S0 ~0,6 + S1 3,5 + S2 4,8 + S3 3,0 giờ, cộng các lần embedding ~1,3 giờ). Bản cuối không cần train thêm.
  - Token chỉ ở `C:\Users\Adminnitrator\.kaggle\` (không ghi vào tài liệu).
  - Push kernel từ **bên trong** thư mục: `PYTHONUTF8=1 .venv/Scripts/kaggle.exe kernels push -p .`, đặt `enable_gpu: true` để push rồi trả về `false`.
  - **Sau mỗi job:** kiểm `COMPLETE`, không còn kernel chạy, `enable_gpu: false`.
  - Code lên Kaggle qua dataset `thinhlai/medicheck-code`: cập nhật bằng `kaggle datasets version` nếu kernel cần code mới. Bản local mới hơn: có `e2e.py`, `export_onnx.py`, `eval.evaluate_e2e_splits`.
- **Local:** `.venv` (Python 3.10, torch 2.6.0+cu124, timm 1.0.30, ultralytics 8.4.204, onnxruntime 1.23.2, kaggle CLI). GPU GTX 1650 4 GB.
  - Chạy module: `.venv/Scripts/python.exe -m medicheck_ai.<tên>`. **Không dùng `-I`**, vì `-I` làm hỏng import `medicheck_ai`. Chỉ dùng `-I -X utf8` cho script nháp.
  - Dùng `--workers 0` (Windows lỗi 1455).
  - Không kill toàn bộ python; chỉ dừng đúng PID.
- `.ocrenv`: môi trường CPU riêng cho Paddle + VietOCR.
- **Test đã dùng một lần** (08/11, mục 14.1): không chạy lại, không chỉnh mô hình hay ngưỡng theo test. Code vẫn khóa (`unseal_test=True`).
- **Repo nhóm** (công khai): https://github.com/thinhlai06/project-AI. Thư mục `D:\project AI` là bản git của repo. `.gitignore` chỉ cho phép đẩy các file `.md` ở thư mục gốc và mô hình cuối (`out/onnx_final/`, `best.pt` + `model.pt` cuối, bảng tra). Đẩy lại sau mỗi lần cập nhật tài liệu. README là trang giới thiệu cho cả nhóm.

---

## 4. Lịch sử thử nghiệm (tóm tắt; số và lý do ở `MediCheck_decisions.md` mục 12)

| Mã | Ngày | Việc | Kết quả chính → quyết định |
|---|---|---|---|
| C1 | 06/11 | Cách chấm điểm trên embedding đóng băng | Loss 107 theo đơn + trừ đối thủ: 62 → 70,9% báo xanh; quy tắc an toàn kép; bỏ kNN |
| C2 | 07/11 | Độ phân giải, TTA | Crop nguồn 512; TTA không đáng chạy chậm 8 lần |
| C2b | 07/11 | So 7 backbone đóng băng | DINOv3 ViT-S/16 CLS 82,1% (DINOv2-S 72,7%) |
| C3 | 07/11 | Kiểm YOLO26/Ultralytics | 2 nhánh train cùng lúc; MuSGD tường minh |
| C4–C6 | 07/11 | Nhãn detector v3, xuất dữ liệu lên Kaggle | 94,9% ảnh truy được box chặt; dataset `medicheck-det`, `medicheck-crops` |
| C7 | 07/11 | Module đánh giá + 7 kiểm thử | Quy tắc đo được; 5 cách chia |
| C9 / S0 | 07/11 | Code train + smoke test Kaggle | Mọi bước đạt; augmentation chuyển lên GPU |
| S1 | 08/11 | D1-A YOLO26s; R1 DINOv3-S vs DINOv2-S | Detector 98,0%; DINOv3 92,6%; DINOv2 trượt an toàn |
| S2 | 08/11 | D2-B ảnh ngoài; R3-B mở toàn bộ; R2-B CosFace; R7 EfficientNet-B0 | Chọn D2-B (98,6%) và R3-B (94,5%); bỏ CosFace; EffNet 85,9% làm mốc |
| local | 08/11 | Cả pipeline (`e2e.py`), cỡ ảnh upload, ONNX | App gửi 2048 px; giao thức cal/ev; mục tiêu fit 1,8% |
| S3 | 08/11 | R3-B seed 1; R5-B ảnh 448 | Seed lệch 0,4; 448 hòa khi chạy thật → bản cuối R3-B seed 1; không chạy S4 |
| local | 08/11 | 7 sơ đồ pipeline (`docs/diagrams/`) | Mermaid + PNG, nhúng vào các file `.md` |
| local | 08/11 | Module suy luận + FastAPI (`backend/`), kiểm trên val | 90,9% báo xanh qua module; bảng tra triển khai đổi sang bảng chỉ lập từ train (138 tên) |
| local | 08/11 | **Test một lần** qua module | **90,2% báo xanh, cận trên 1,09% / 1,31%** → đạt |

---

## 5. File và thư mục quan trọng

| Đường dẫn | Nội dung |
|---|---|
| `out/onnx_final/` | **Bản cuối triển khai**: `detector.onnx`, `recognizer.onnx`, `deploy_config.json`, `export.json` |
| `out/s2/det/d2b/weights/best.pt` | Detector cuối (PyTorch) + `eval_val.json`, dự đoán val/VAIPE-test |
| `out/s3/r3b_seed1/model.pt` | Bộ nhận dạng cuối (PyTorch) + `final.json`, `log.jsonl` |
| `out/s1/`, `out/s2/`, `out/s3/` | Output các phiên Kaggle (mọi nhánh, log, `summary.json`, `gpu_monitor.csv`) |
| `out/e2e_s1/`, `out/e2e_s2/`, `out/e2e_s3_seed1/`, `out/e2e_s3_448/` | Kết quả cả pipeline (`e2e_orig2048*.json`), crop từ detector |
| `out/v2/` | Nhãn v2, bộ chia v2, `lookup_name_classes.csv` (141 tên, lập từ **mọi fold**: chỉ để tham khảo, không dùng để triển khai hay đo) |
| `out/v3det/` | Nhãn detector v3 |
| `backend/` | **Máy chủ AI** (lên repo): `medicheck_server/infer.py` (module), `app.py` (FastAPI), `API.md`, `requirements.txt`, `tests/` |
| `out/infer_val/`, `out/infer_test/` | Kiểm module trên val và **kết quả test chính thức** (`validate.json`, `red_raw.npz`, cache) |
| `medicheck_ai/` | `eval.py`, `recognizer.py`, `detector.py`, `e2e.py`, `export_onnx.py`, `validate_infer.py` (chỉ ở máy local) |
| `tests/test_eval.py` | 7 kiểm thử (chạy: `.venv/Scripts/python.exe tests/test_eval.py`) |
| `kaggle/` | Script kernel các phiên (`medicheck-s1..s3`, smoke, embed, backbones) và thư mục nguồn dataset |
| `scripts/` | Tiền xử lý dữ liệu và thử nghiệm C1–C2b |
| `docs/diagrams/` | 7 sơ đồ pipeline: `.mmd` (nguồn Mermaid, sửa được) + `.png` (nhúng vào các file `.md`, dán được vào báo cáo). Sửa pipeline thì sửa `.mmd` rồi render lại: `npx -p @mermaid-js/mermaid-cli@11.4.2 mmdc -i x.mmd -o x.png -s 2 -b white` |
| `BAO_CAO_CONG_VIEC.md` | Báo cáo ngắn (~100 từ) sau mỗi task cho người dùng |

---

## 6. Hàng đợi đồng bộ báo cáo `.docx` (chưa đưa vào báo cáo v5)

1. **Nền tảng train:** Colab → Kaggle 2 × T4 (2.3.3, 3.1, Bảng 2.9, Hình 2.7).
2. **Detector:** YOLO26s, MuSGD lr0 0,01, batch 32 (Bảng 2.7); nhãn detector v3 từ bộ bổ trợ (2.2.1 Bảng 2.3, 2.2.3, 2.2.4); thêm Negatives + ảnh ngoài vào train; nhánh NMS, ngưỡng 0,5; crop suy luận lề 13%.
3. **Bộ nhận dạng:** DINOv3 ViT-S/16 token CLS, crop nguồn 512, ảnh vào 384, mở toàn bộ + LLRD 0,75. Sửa 1.7.2, Hình 1.7, 2.3.1, Bảng 2.7, Bảng 1.1/1.2. Thêm tài liệu DINOv3 (Siméoni et al. 2025, đối chiếu câu gốc, vẫn ≤ 15 tài liệu) và giới hạn giấy phép.
4. **Huấn luyện:** 2 giai đoạn, augmentation trên GPU, checkpoint cuối (2.3.3, 3.1). Loss 107 có điều kiện theo đơn (2.3.2/2.3.3). Số smoke test 2 epoch không đưa vào như kết quả.
5. **Quyết định và an toàn:**
   - điểm trừ đối thủ 0,5 (2.4.3, 2.4.4);
   - quy tắc an toàn kép (2.3.4, 3.3);
   - "quy tắc đo được" thay "low-evidence classes" (2.3.4, Bảng 2.8);
   - giao thức cal/ev 5 cách chia;
   - số chính thức là cả pipeline;
   - ngưỡng fit với mục tiêu 1,8% (2.4.x, 3.3).
6. **Kế hoạch thực nghiệm:** A/B một yếu tố mỗi lần, quy tắc hòa 1,5 điểm, các A/B đã bỏ và lý do, đo độ dao động seed (3.1).
7. **Kết quả:**
   - bảng thử nghiệm C1, C2b;
   - bảng S1–S3 (detector D1-A/D2-B, bộ nhận dạng R1–R7, seed, 448, ghép mô hình);
   - cả pipeline 89,5%, cỡ ảnh upload 2048 px;
   - độ trễ ONNX (3.4–3.6; Bảng 3.5, 3.6 đang trống).
8. **Triển khai:** API nhận ảnh 2048 px JPEG q85; máy chủ chỉ CPU; `deploy_config.json` (2.x API, 2.x triển khai).
9. **OCR:** tách thêm chẩn đoán, hiển thị "Bệnh: …"; trường `prescription.diagnosis_text` (2.x OCR/parser, bảng database).
10. **Giới hạn mới (3.7):**
    - viên lạ cùng nguồn;
    - AGPL-3.0, DINOv3 License;
    - số val lạc quan nhẹ do chọn trên val;
    - ~17% ảnh có viên nền không nhãn.
11. **Số test (đã có):** 90,2% báo xanh, cận trên 1,09% / 1,31%, detector đếm đúng 98,5%. Điền vào bảng kết quả, Bảng 3.5/3.6, dòng "Content to be updated" ở kết luận.
12. Module suy luận + API (`backend/`), sơ đồ `docs/diagrams/` (dán làm hình), giới hạn báo đỏ oan 1,4% trên test.
