# Dữ liệu

> **Trả lời câu hỏi:** mô hình học từ dữ liệu nào, chia ra sao, có vấn đề gì, tạo lại thế nào.
> Phân tích đầy đủ: `docs/archive/vaipe_analysis.md`. Cập nhật: 2026-11-14.

## 1. Nguồn

| Bộ | Nội dung | Dùng cho | Giấy phép |
|---|---|---|---|
| **VAIPE_PILL** (Hugging Face `Elfsong/VAIPE_PILL`, dữ liệu cuộc thi AI4VN 2022) | 9.502 ảnh viên (32.828 box, 107 lớp + lớp 107 "ngoài đơn"), 1.173 đơn (2 mẫu BHYT, 141 tên thuốc), bảng nối ảnh ↔ đơn | Detector, bộ nhận dạng, OCR (đánh giá) | Theo điều khoản cuộc thi |
| Kaggle `alexanderyyy/pills-detection-dataset` | 12.067 ảnh, 1 lớp "pill", gồm box chặt gán lại cho ảnh VAIPE | Chỉ detector (nhãn v3, ảnh nền trống, ảnh ngoài) | CC BY-NC-SA 4.0 |

Không dùng: MEDISEG, ePillID (thuốc nước ngoài), NIH RxImage, CURE; VAIPE đầy đủ (không có nguồn tải công khai). Không gán nhãn tay, không thu thập mới.

## 2. Sự thật quan trọng

- Bbox VAIPE nằm trong hệ tọa độ **đã xoay EXIF**; hơn nửa số ảnh cần xoay.
- Lớp 107 = viên không thuộc đơn của ảnh (kể cả viên của lớp đã biết).
- Một tên thuốc có thể ứng với nhiều lớp viên (biệt dược tương đương), và ngược lại.
- Màu viên trong ảnh không ổn định → không dùng màu để mô tả.
- 12,6% đơn có dòng thiếu lịch; 61 dòng nửa viên; vài dòng "khi cần".
- Đơn là ảnh chụp màn hình PDF sạch, không phải ảnh chụp giấy.

## 3. Chia train/val/test (bộ chia v2, theo nhóm đơn gần trùng)

| Phần | Ảnh | Đơn | Nhóm | Box nhận dạng | Lớp |
|---|---|---|---|---|---|
| Train | 6.256 | 585 | 503 | 17.179 | 107 |
| Val | 1.604 | 294 | 269 | 3.586 | 93 |
| Test (đã dùng một lần) | 1.576 | 294 | 266 | 3.460 | 86 |
| Giữ riêng theo ảnh | 66 | 8 | 8 | 150 | 18 |

Không nhóm đơn nào nằm ở nhiều phần. File: `out/v2/split.csv`, `out/groups.csv`.

## 4. Sửa nhãn

- **Nhãn v2** (bộ nhận dạng): chuyển 76 box Tydol từ lớp 1 sang 60; sửa mapping đơn 119, 120; loại 55 box ngoài đơn (đơn 574, 575, 1168) khỏi bộ nhận dạng; bỏ dòng Paracetamol đơn 708 khỏi bảng tra. File `out/v2/`.
- **Nhãn v3** (detector): box chặt truy từ bộ bổ trợ cho 94,9% ảnh VAIPE. File `out/v3det/`.

## 5. Tạo lại từ đầu

Dữ liệu thô không nằm trong repo. Chuỗi script (máy của phụ trách AI, thư mục `scripts/`, chạy theo thứ tự):

`download` → `extract_assets` → `analyze_pres` → `embed` → `neardup` → `make_splits` → `fix_labels` → `make_splits_v2` → `map_reannot` → `map_reannot_pass2` → `build_v3det` → `export_detector` → `extract_crops_hr`; train trên Kaggle (`kaggle/medicheck-s1…s3`); xuất mô hình `medicheck_ai.export_onnx`, `scripts/export_ocr_onnx.py`, `scripts/split_onnx_weights.py`.
