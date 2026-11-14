# Thuật ngữ

Dùng **đúng** các từ này trong tài liệu, code, câu chữ của app. Cột "Trong code" là tên dùng trong API, database và Dart.

| Thuật ngữ | Trong code | Nghĩa |
|---|---|---|
| Đơn (đơn thuốc) | `prescription` | Một đơn BHYT đã nhập và xác nhận |
| Dòng thuốc | `drug_line` | Một thuốc trên đơn: tên, số lượng, lịch, ghi chú |
| Tên đọc được | `raw_name` | Chữ OCR đọc từ đơn, để hiển thị |
| Tên danh mục | `matched_name` / `name` | Tên đã khớp với danh mục 138 tên; gửi đúng chuỗi này cho `/v1/pills/verify` |
| Danh mục | `catalog` | 138 tên thuốc kiểm được bằng hình (`GET /v1/catalog`) |
| Buổi | `session`: `sang`, `trua`, `chieu`, `toi` | Sáng, trưa, chiều, tối |
| Đơn đang dùng | `prescription.status = active` | Đơn duy nhất đang được nhắc và kiểm (BR-12); đơn cũ là `ended` |
| Ảnh đơn gốc | `prescription.image_path` | File ảnh/PDF đơn lưu trong thư mục riêng của app để gửi người thân (ADR-016) |
| Phiếu đơn | – | Ảnh bảng chữ to app vẽ từ các dòng thuốc để gửi người thân (SCR-SHARE) |
| Cữ | `dose_event` | Lần uống của một buổi trong một ngày, theo đơn đang dùng |
| Lịch uống | `dose_schedule` | Số viên của một dòng thuốc ở một buổi |
| Kiểu liều | `dose_type`: `regular`, `half_pill`, `as_needed`, `missing_schedule` | Thường; nửa viên; khi cần; thiếu lịch |
| Chấm ảnh / chỉ nhắc lịch | `check_mode`: `image`, `reminder_only` | Dòng được kiểm bằng ảnh, hoặc chỉ được nhắc |
| Kiểm thuốc / lượt kiểm | `verification_attempt` | Một lần chụp và gửi ảnh cữ; tối đa 2 lượt mỗi cữ |
| Xanh / đỏ / vàng | `green` / `red` / `yellow` | Khớp đơn / sai cữ hoặc ngoài đơn / chưa chắc, hãy kiểm vỏ hộp |
| Cữ xanh / một phần / chưa xanh | `green` / `partial` / `not_green` | Trạng thái cả cữ do server trả |
| Khung chụp | `frame` | Vùng trên ảnh mà app đếm viên |
| Tự kiểm vỏ hộp | `confirm_type = self_confirmed` | Người dùng tự xác nhận khi app không báo xanh |
| App xác nhận | `confirm_type = app_verified` | Cữ được ghi nhận sau khi server báo xanh |
| Viên lạ đã biết | – | Viên của lớp đã biết nhưng không thuộc đơn |
| Lớp 107 | – | Nhãn VAIPE cho viên không thuộc đơn của ảnh |
| Lớp đo được | `measurable_classes` | 93 lớp được phép báo xanh; 14 lớp còn lại luôn vàng |
| Cận trên chấp nhận nhầm | `far_hi` | Cận trên 95% của tỉ lệ báo xanh khi có viên sai; chuẩn ≤ 2% |
| Tập test (khóa) | `fold = test` | Dữ liệu chỉ chạy một lần với bản cuối; đã dùng |
| Server AI | `backend/medicheck_server` | FastAPI chạy mô hình trên CPU laptop |
| Máy giả lập | emulator | Android Virtual Device trên laptop |
