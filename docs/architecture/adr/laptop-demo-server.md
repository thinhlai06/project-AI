# ADR-004: Laptop làm server khi demo, không cloud (điểm "không Docker" đã bị ADR-017 thay)

- **Trạng thái:** Bị thay thế một phần bởi ADR-017 (chỉ điểm "không Docker")
- **Ngày:** 2026-11-14 (xác nhận lại quyết định 2026-11-08 "không dùng Hugging Face Spaces")
- **Người quyết:** phụ trách AI

## Bối cảnh

Nhóm không có server và chưa có kinh nghiệm vận hành server. Laptop dùng để trình bày khác máy phát triển. Server chỉ cần CPU: ~1–2 giây mỗi lần kiểm thuốc, ~5 giây mỗi đơn. Ảnh đơn chứa dữ liệu sức khỏe.

## Quyết định

- Server chạy trên **laptop trình bày** bằng Python venv (`pip install -r backend/requirements.txt`, `uvicorn …`). Hướng dẫn: [../deployment.md](../deployment.md).
- App trên máy giả lập gọi `http://10.0.2.2:8000`; điện thoại thật gọi IP laptop qua hotspot; tunnel HTTPS (`cloudflared`) là dự phòng.
- **Không dùng Docker** ở MVP.

## Phương án đã cân nhắc

| Phương án | Vì sao không chọn |
|---|---|
| Docker Desktop trên laptop | Windows cần bật ảo hóa trong BIOS + WSL2; thêm rủi ro trên máy lạ ngay trước buổi trình bày; server không có database nên Docker không gỡ được khó khăn nào |
| Cloud miễn phí (Hugging Face Spaces, cần Docker) | Gửi ảnh đơn cho bên thứ ba; máy ngủ khi không dùng, lần gọi đầu chậm; phụ thuộc Internet của phòng trình bày |
| Thuê VPS | Tốn tiền, phải quản trị; không cần cho môn học |

## Hệ quả

- Miễn phí, chạy được khi không có Internet, dữ liệu không rời laptop.
- Phải đo tốc độ trên chính laptop trình bày (cổng 22/11).
- Thêm `Dockerfile` sau này không cần sửa code (server không trạng thái), nếu nhóm muốn đưa lên cloud.
