# ADR-014: App gửi ảnh 2048 px JPEG q85

- **Trạng thái:** Đã chấp nhận
- **Ngày:** 2026-11-08
- **Người quyết:** phụ trách AI

## Quyết định

App xoay ảnh theo EXIF, thu cạnh dài về **2048 px**, nén **JPEG chất lượng 85** (~290 KB) rồi gửi. Đây đúng là đường đi đã dùng khi đo cả chuỗi trên val và test.

## Phương án đã cân nhắc

| Phương án | Vì sao không chọn |
|---|---|
| Gửi ảnh gốc 12 MP | 3–5 MB mỗi lần, chậm trên 4G; không cải thiện kết quả |
| Thu nhỏ hơn (1280 px) | Crop viên nhỏ, giảm nhận dạng; không phải cỡ đã đo |

## Hệ quả

- Tải lên < 1 giây; server vẫn tự thu nhỏ ảnh lớn hơn.
- App phải chuẩn bị ảnh trong isolate để không đứng giao diện (ví dụ Dart trong `backend/API.md`).
