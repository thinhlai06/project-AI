# ADR-017: Đóng gói server bằng Docker (Docker Compose)

- **Trạng thái:** Đã chấp nhận
- **Ngày:** 2026-11-15
- **Người quyết:** chủ dự án
- **Thay thế:** [ADR-004](laptop-demo-server.md) (chỉ ở điểm "không Docker"; laptop vẫn là nơi chạy server, vẫn không cloud)

## Bối cảnh

Máy phát triển (PC) khác máy trình bày (laptop). Laptop sẽ `git clone` repo rồi chạy. Cách cài Python + venv bằng tay có nhiều chỗ lỗi trên máy lạ: sai phiên bản Python, đường dẫn dài, thiếu thư viện hệ thống.

## Quyết định

- Server chạy trong container: `docker compose up --build` từ thư mục gốc repo. Chạy thử ngày 2026-11-15: image 1,5 GB, container `healthy`, `/health`, `/v1/catalog`, `/v1/pills/verify`, `/v1/prescriptions/parse` đều trả đúng.
- `Dockerfile` (Python 3.12-slim, chạy bằng user không phải root, có `HEALTHCHECK`), `.dockerignore` (danh sách cho phép: chỉ `backend/` và `out/onnx_final/`, không có `detector.pt`), `docker-compose.yml` ở thư mục gốc.
- Mô hình nằm **trong image** (copy từ repo); không dùng volume, để clone về là chạy.
- Cổng `8000` mở ra máy chủ: máy giả lập gọi `http://10.0.2.2:8000`, điện thoại thật gọi `http://<IP laptop>:8000`, giống trước.
- **Cách chạy bằng venv giữ làm phương án dự phòng** ([../deployment.md](../deployment.md) mục 2b): dùng khi Docker Desktop không chạy được trên laptop.
- Vẫn không dùng cloud (ảnh đơn là dữ liệu sức khỏe).

## Hệ quả

- Laptop cần Docker Desktop (Windows: bật ảo hóa trong BIOS, WSL2). **Phải kiểm trên chính laptop trình bày sớm**, không để sát buổi trình bày.
- Docker Desktop và máy giả lập Android cùng dùng ảo hóa và cùng chiếm RAM; laptop nên có ≥ 16 GB RAM, hoặc giới hạn WSL2 bằng `%UserProfile%\.wslconfig` (`memory=4GB`).
- Lần build đầu cần Internet (tải image nền và thư viện, khoảng 1 GB); sau đó chạy không cần Internet. Nên build sẵn ở nhà, rồi `docker compose up` ở nơi trình bày.
- Đổi `requirements.txt` hoặc mô hình thì phải build lại image.
