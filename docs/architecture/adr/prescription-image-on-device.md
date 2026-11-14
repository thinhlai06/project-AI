# ADR-016: Lưu ảnh đơn gốc trên điện thoại để gửi người thân

- **Trạng thái:** Đã chấp nhận
- **Ngày:** 2026-11-15
- **Người quyết:** phụ trách sản phẩm
- **Thay thế:** [ADR-012](privacy-no-images-stored.md)

## Bối cảnh

ADR-012 cấm lưu mọi ảnh. Tính năng "Gửi người thân" (FR-PRES-09) cần gửi kèm ảnh đơn gốc để người thân so với phiếu app đọc được, và cần gửi lại được từ chi tiết đơn, không chỉ ngay lúc nhập. Server không trả vị trí họ tên và số BHYT nên app không che được các vùng này trên ảnh.

## Quyết định

- **Ảnh đơn gốc** (ảnh hoặc PDF người dùng đã chọn/chụp) được lưu **một bản** trong thư mục riêng của app (`<app documents>/prescriptions/<prescription_id>.<jpg|png|pdf>`), đường dẫn tương đối ghi ở `prescription.image_path`.
  - Xóa đơn → xóa file. Đơn `ended` vẫn giữ file cho đến khi xóa đơn.
  - Không đưa vào thư viện ảnh của máy, không sao lưu lên đám mây của app.
  - Ảnh đơn chỉ rời máy hai lần: gửi server để đọc đơn, và khi người dùng tự bấm "Gửi người thân".
  - Trước khi mở bảng chia sẻ, app luôn hiện: "Ảnh đơn có họ tên và số BHYT của bác. Chỉ gửi cho người thân tin cậy."
- **Ảnh thuốc**: không lưu ở đâu cả (giữ như ADR-012). Màn kết quả vẽ box lên ảnh trong bộ nhớ, rời màn là bỏ.
- **Họ tên, số BHYT**: không lưu dạng chữ (server không trả các trường này).
- **Chẩn đoán**: chỉ lưu trên điện thoại, xóa cùng đơn.
- **Server**: xử lý trong bộ nhớ rồi bỏ; không ghi ảnh ra đĩa; không log nội dung đơn.
- Ảnh chỉ gửi tới địa chỉ server người dùng cấu hình.

## Phương án đã cân nhắc

| Phương án | Vì sao không chọn |
|---|---|
| Giữ ADR-012, chỉ gửi người thân ngay lúc nhập | Không gửi lại được sau đó; người cao tuổi thường nhờ người thân kiểm khi đã dùng vài ngày |
| Che họ tên/BHYT trên ảnh rồi mới lưu | Server không trả vị trí các trường này; phải thêm mô hình, ngoài phạm vi MVP |
| Chỉ gửi chữ | Người thân không có gì để đối chiếu với đơn gốc |

## Hệ quả

- ERD có thêm `prescription.image_path` và `image_mime`; ST-07 lưu file, ST-09 xóa file (FR-PRES-10).
- Cần `path_provider` (thêm vào [ADR-015](flutter-app-stack.md)).
- Database và file ảnh chưa mã hóa ở MVP; ghi vào giới hạn của báo cáo.
- Dùng tunnel hay cloud thì ảnh đi qua bên thứ ba: chỉ dùng với dữ liệu mẫu.
