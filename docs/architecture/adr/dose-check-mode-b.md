# ADR-011: Kiểm cả cữ trong một ảnh (chế độ B)

- **Trạng thái:** Đã chấp nhận
- **Ngày:** 2026-10-22
- **Người quyết:** nhóm sản phẩm

## Quyết định

Người dùng đặt **đúng những viên sắp uống của cữ** lên lòng bàn tay rồi chụp một ảnh. App so tập viên phát hiện được với tập kỳ vọng (loại và số lượng), báo thiếu/thừa. Lòng bàn tay là hướng dẫn chính (VAIPE có cả ảnh tay và mặt phẳng); app chỉ đếm viên có tâm trong khung chụp.

## Phương án đã cân nhắc

| Phương án | Vì sao không chọn |
|---|---|
| Chế độ A: chụp 1 viên mỗi loại | Người dùng phải lấy thuốc hai lần; không kiểm được số lượng |
| Chụp vỉ/hộp thuốc | Không có dữ liệu vỉ/hộp; không phải viên sắp uống thật |

## Hệ quả

- Một lần chụp kiểm cả loại lẫn số lượng: mỗi cữ 3 chạm (thông báo → chụp → "Tôi đã uống").
- Viên chồng nhau hoặc bị ngón tay che sẽ thành vàng; hướng dẫn "các viên rời nhau".
