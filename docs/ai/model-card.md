# Model card – AI kiểm thuốc và đọc đơn

> **Trả lời câu hỏi:** mô hình nào đang chạy, dùng cho việc gì, giỏi đến đâu, không được dùng vào đâu.
> Bản chốt: **`final-2026-11-08`** (`out/onnx_final/deploy_config.json`). Quyết định: [ADR-005 … ADR-010, ADR-013, ADR-014](../architecture/adr/README.md). Dữ liệu: [dataset.md](dataset.md).
> Cập nhật: 2026-11-14 · Trạng thái: **đã chốt** (không train thêm)

## 1. Mục đích sử dụng

| | |
|---|---|
| **Dùng cho** | Kiểm các viên của một cữ có khớp đơn BHYT không (danh mục đóng VAIPE); đọc đơn BHYT bệnh viện (2 mẫu VAIPE) thành dòng thuốc và lịch |
| **Người dùng** | Người cao tuổi tự dùng, qua app có màn xác nhận và lối thoát "kiểm vỏ hộp" |
| **Không dùng cho** | Thay dược sĩ; kiểm thuốc ngoài 138 tên; kiểm hàm lượng; đơn ngoài 2 mẫu VAIPE; quyết định lâm sàng; chẩn đoán |

## 2. Thành phần và file

| Thành phần | Mô hình | File (`out/onnx_final/`) | Vào → ra | Tốc độ CPU |
|---|---|---|---|---|
| Detector | YOLO26s, 1 lớp "pill", NMS, ngưỡng 0,5 | `detector.onnx` (36 MB) | `images [1,3,640,640]` letterbox RGB 0–1 → `output0 [1,300,6]` (x1,y1,x2,y2,conf,cls) | ~120–140 ms/ảnh |
| Bộ nhận dạng | DINOv3 ViT-S/16 (~21 triệu tham số) + đầu cosine 107 lớp | `recognizer.onnx` (83 MB) | `image [n,3,384,384]` (crop đệm xám, chuẩn hóa ImageNet) → `embedding [n,384]`, `cosine [n,107]` | ~170–190 ms/viên |
| Tìm dòng chữ | PP-OCRv5 mobile det | `ocr/det.onnx` | ảnh đơn → box dòng chữ | |
| Đọc chữ | VietOCR `vgg_transformer` (encoder + decoder, giải mã tham lam) | `ocr/rec_encoder.onnx` (+ `.weights1/2`), `ocr/rec_decoder.onnx`, `ocr/rec_vocab.json` | ảnh dòng chữ → chuỗi | ~5 giây/đơn cả chuỗi |
| Bảng tra | tên thuốc → tập lớp viên được phép, 138 tên, **chỉ lập từ train** | `lookup_name_classes.csv` | | |
| Tham số triển khai | ngưỡng, lề crop, lớp đo được, cỡ ảnh | `deploy_config.json` | | |

Bản PyTorch nguồn: `out/s2/det/d2b/weights/best.pt` (detector), `out/s3/r3b_seed1/model.pt` (bộ nhận dạng). Bản ONNX đã kiểm khớp PyTorch (`export.json`).

## 3. Logic quyết định (không phải mô hình học)

| Tham số | Giá trị |
|---|---|
| Lề crop | 13% cạnh dài, crop nguồn tối đa 512 px |
| Điểm của viên với dòng thuốc | cosine(lớp được phép) − 0,5 × cosine(đối thủ ngoài đơn) |
| Ghép viên ↔ dòng | `scipy.optimize.linear_sum_assignment` |
| Ngưỡng xanh | 0,0529 (fit trên crop nhãn thật của val, mục tiêu cận trên 1,8%) |
| Lớp được báo xanh | 93 lớp đo được; 14 lớp chỉ có ở 1 nhóm đơn luôn vàng |
| Đỏ "cữ khác" / "ngoài đơn" | 0,0529 / 0,30 (chỉ là lời khuyên, không làm cữ xanh) |
| Ảnh tối / mờ | độ sáng < 50 / độ nét Laplacian < 4 (chỉ thêm lời khuyên) |

## 4. Kết quả

**Test – chạy một lần, số chính thức** (kiểm thuốc 2026-11-08, 1.230 cảnh; OCR 2026-11-09, 294 đơn, 655 dòng):

| Chỉ số | Giá trị | Chuẩn |
|---|---|---|
| Cữ đúng được báo xanh | **90,2%** | ≥ 70% |
| Cận trên 95% báo xanh nhầm – viên ngoài đơn (lớp 107) | **1,09%** | ≤ 2% |
| Cận trên 95% báo xanh nhầm – viên lạ đã biết | **1,31%** | ≤ 2% |
| Detector đếm đúng số viên | 98,5% | |
| Viên đúng bị báo đỏ oan | 1,40% | (mô tả) |
| OCR: dòng thuốc đúng hoàn toàn – ảnh gốc / mô phỏng chụp giấy | **99,85% / 98,93%** | |
| OCR: đơn đúng hoàn toàn – ảnh gốc / mô phỏng | 99,66% / 97,96% | |

**Val** (dùng để chọn): báo xanh 90,9% qua server, cận trên 1,19% / 1,79%; nhận đúng trong ứng viên 95,8%; mốc CNN EfficientNet-B0 85,9% báo xanh.

## 5. Giới hạn đã biết

- Chỉ phủ danh mục 138 tên của một hệ thống bệnh viện; thuốc ngoài danh mục chỉ nhắc lịch.
- Tập test cùng nguồn chụp với train; viên lạ dùng khi đo cùng nguồn dữ liệu, nên số an toàn có thể lạc quan với thuốc hoàn toàn mới.
- **Chưa thử trên ảnh chụp giấy thật** và chưa thử với người dùng cao tuổi thật.
- Không kiểm hàm lượng; lớp 2, 37, 40, 104 gộp nhiều thuốc/hàm lượng.
- Nhãn sửa bằng luật + so ảnh, không có chuyên gia dược xác nhận; ~17% ảnh còn viên ở nền không có nhãn.
- Báo đỏ oan cao hơn trên test (1,40%) so với val (0,11%).

## 6. Giấy phép

| Thành phần | Giấy phép | Nghĩa vụ |
|---|---|---|
| `ultralytics`, trọng số YOLO26 | AGPL-3.0 | Phát hành dịch vụ phải công khai mã nguồn backend |
| DINOv3 | DINOv3 License (Meta) | Kèm [LICENSE-DINOv3.md](../../LICENSE-DINOv3.md); công bố phải ghi nhận DINOv3 |
| Bộ bổ trợ `alexanderyyy/pills-detection-dataset` | CC BY-NC-SA 4.0 | Không thương mại |
| PP-OCRv5, VietOCR | Chưa kiểm | **Việc mở:** kiểm giấy phép trước khi phát hành |

## 7. Quy tắc thay đổi

Không sửa `deploy_config.json`, bảng tra hay file ONNX bằng tay. Mọi thay đổi mô hình phải đo lại trên val theo giao thức ở [ADR-008](../architecture/adr/safety-rule-and-sealed-test.md), có tập test mới, và đổi `version`.
