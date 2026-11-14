# Architecture Decision Records (ADR)

Mỗi ADR ghi **một** quyết định quan trọng: bối cảnh, lựa chọn, phương án đã loại và hệ quả. ADR giúp người mới (và AI agent) biết *vì sao* hệ thống như hiện tại, để không vô tình làm ngược quyết định cũ.

## Quy ước

- **Tên file** đặt theo nội dung (kebab-case, không đánh số). **Mã** `ADR-NNN` nằm trong file và trong bảng dưới; mã không bao giờ dùng lại.
- **Trạng thái:** `Đề xuất` → `Đã chấp nhận` → (`Bị thay thế bởi ADR-xxx` | `Hủy`). Không sửa nội dung một ADR đã chấp nhận; muốn đổi thì viết ADR mới và đánh dấu ADR cũ bị thay thế.
- **Khuôn:** chép [template.md](template.md).
- Bằng chứng số liệu chi tiết nằm ở `docs/archive/MediCheck_decisions.md` (sổ quyết định cũ, mục 12–15).

## Danh sách

| Mã | Quyết định | Trạng thái | Ngày |
|---|---|---|---|
| ADR-001 | [Suy luận trên server, app không chạy mô hình](server-side-inference.md) | Đã chấp nhận | 2026-11-08 |
| ADR-002 | [Flutter, demo chính trên máy giả lập Android, giữ đường iOS](flutter-android-first.md) | Đã chấp nhận | 2026-11-15 |
| ADR-003 | [Dữ liệu cục bộ, không tài khoản, server không database](local-first-no-accounts.md) | Đã chấp nhận | 2026-11-03 |
| ADR-004 | [Laptop làm server khi demo, không Docker, không cloud](laptop-demo-server.md) | Đã chấp nhận | 2026-11-15 |
| ADR-005 | [Danh mục đóng + bộ nhận dạng embedding](closed-catalog-embedding-recognizer.md) | Đã chấp nhận | 2026-11-03 |
| ADR-006 | [Detector YOLO26s nhánh NMS](yolo26s-detector.md) | Đã chấp nhận | 2026-11-08 |
| ADR-007 | [Bộ nhận dạng DINOv3 ViT-S/16](dinov3-recognizer.md) | Đã chấp nhận | 2026-11-08 |
| ADR-008 | [Chuẩn an toàn ≤ 2% và tập test dùng một lần](safety-rule-and-sealed-test.md) | Đã chấp nhận | 2026-11-06 |
| ADR-009 | [Ba trạng thái xanh/đỏ/vàng, không mô tả màu, không đoán](result-states.md) | Đã chấp nhận | 2026-11-08 |
| ADR-010 | [OCR bằng PP-OCRv5 + VietOCR (ONNX) + luật tách trường](ocr-onnx-rule-parser.md) | Đã chấp nhận | 2026-11-09 |
| ADR-011 | [Kiểm cả cữ trong một ảnh (chế độ B)](dose-check-mode-b.md) | Đã chấp nhận | 2026-10-22 |
| ADR-012 | [Không lưu ảnh và thông tin định danh](privacy-no-images-stored.md) | Bị thay thế bởi ADR-016 | 2026-11-03 |
| ADR-013 | [Bảng tra tên → lớp chỉ lập từ tập train](train-only-lookup.md) | Đã chấp nhận | 2026-11-08 |
| ADR-014 | [App gửi ảnh 2048 px JPEG q85](upload-2048-jpeg.md) | Đã chấp nhận | 2026-11-08 |
| ADR-015 | [Bộ thư viện app: Riverpod, go_router, drift, http](flutter-app-stack.md) | Đã chấp nhận | 2026-11-15 |
| ADR-016 | [Lưu ảnh đơn gốc trên điện thoại để gửi người thân (thay ADR-012)](prescription-image-on-device.md) | Đã chấp nhận | 2026-11-15 |
