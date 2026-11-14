# ADR-003: Dữ liệu cục bộ, không tài khoản, server không database

- **Trạng thái:** Đã chấp nhận
- **Ngày:** 2026-11-03
- **Người quyết:** phụ trách AI, nhóm mobile

## Bối cảnh

Một người dùng trên một máy; nhắc thuốc phải chạy khi mất mạng; dữ liệu là thông tin sức khỏe nhạy cảm; nhóm không có người làm backend.

## Quyết định

- Dữ liệu ở **SQLite trên điện thoại** qua `drift` (truy vấn kiểu an toàn, có migration). Schema: [../erd.md](../erd.md).
- Không đăng ký, không đăng nhập, không đồng bộ đám mây.
- Server **không trạng thái**: không database; danh mục, trọng số và cấu hình là file có phiên bản, nạp khi khởi động.

## Phương án đã cân nhắc

| Phương án | Vì sao không chọn |
|---|---|
| Firebase / Supabase | Đưa dữ liệu sức khỏe lên cloud, cần tài khoản, thêm việc mà MVP không cần |
| Database trên server | Phải bảo mật, sao lưu, quản lý người dùng; không có người làm |
| `sqflite` thuần / Hive / Isar | `drift` có kiểu an toàn và migration rõ ràng cho dữ liệu quan hệ |

## Hệ quả

- Đổi máy hoặc gỡ app là mất dữ liệu (chấp nhận ở MVP).
- Database chưa mã hóa, dựa vào sandbox của hệ điều hành (ghi vào giới hạn).
- Chế độ người thân theo dõi từ xa sẽ cần quyết định mới (giai đoạn 2).
