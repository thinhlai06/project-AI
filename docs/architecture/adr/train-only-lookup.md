# ADR-013: Bảng tra tên → lớp chỉ lập từ tập train

- **Trạng thái:** Đã chấp nhận
- **Ngày:** 2026-11-08
- **Người quyết:** phụ trách AI

## Bối cảnh

Server cần biết tên thuốc trên đơn ứng với lớp viên nào. Bảng `out/v2/lookup_name_classes.csv` (141 tên) được lập từ **mọi fold**, kể cả test.

## Quyết định

Server dùng `out/onnx_final/lookup_name_classes.csv`: **138 tên, chỉ lập từ train**, đúng bảng đã dùng khi đo an toàn. OCR khớp tên vào chính danh mục này; `GET /v1/catalog` trả đúng 138 tên.

## Hệ quả

- Không rò rỉ nhãn test; server giống hệt cái đã đo.
- 3 tên (menison 4mg, otdxicam 7.5mg, vitaminad) thành "chỉ nhắc lịch".
- App phải gửi `name` **đúng chuỗi** server trả (đã chuẩn hóa chữ thường), không gửi chữ OCR thô.
