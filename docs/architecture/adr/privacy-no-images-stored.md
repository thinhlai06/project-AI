# ADR-012: Không lưu ảnh và thông tin định danh

- **Trạng thái:** Bị thay thế bởi ADR-016 (2026-11-15)
- **Ngày:** 2026-11-03
- **Người quyết:** nhóm sản phẩm

## Quyết định

- Không lưu ảnh đơn, ảnh thuốc, họ tên, số BHYT ở cả điện thoại và server.
- Chẩn đoán là dữ liệu sức khỏe nhạy cảm: chỉ lưu trên điện thoại, xóa cùng đơn, chỉ rời máy trong lần gửi ảnh đơn để OCR.
- Server xử lý trong bộ nhớ rồi bỏ; không log nội dung đơn.
- Ảnh chỉ gửi tới địa chỉ server người dùng cấu hình.

## Hệ quả

- Màn kết quả chỉ vẽ box lên ảnh đang giữ trong bộ nhớ; lịch sử chỉ có chữ và trạng thái.
- Không làm được tính năng "xem lại ảnh cũ" (chấp nhận).
- Database chưa mã hóa ở MVP (ghi vào giới hạn).
- Dùng tunnel hay cloud thì ảnh đi qua bên thứ ba: chỉ dùng với dữ liệu mẫu.
