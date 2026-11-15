# Triển khai và chạy demo

> **Trả lời câu hỏi:** chạy server ở đâu, app nối vào bằng cách nào, trước buổi trình bày cần kiểm gì.
> Quyết định: [ADR-004](adr/laptop-demo-server.md) (laptop làm server, không cloud) và [ADR-017](adr/docker-server.md) (đóng gói bằng Docker).
> Cập nhật: 2026-11-15 · Trạng thái: **đã chốt**

## 1. Bố trí

```mermaid
flowchart LR
  subgraph Laptop trình bày [Laptop trình bày (Windows)]
    SRV[Server AI<br/>Docker :8000]
    EMU[Máy giả lập Android<br/>app MediCheck]
    CAM[(Webcam)]
  end
  PH[iPhone / điện thoại thật<br/>nếu cài được app] -. "Wi-Fi / hotspot<br/>http://IP-laptop:8000" .-> SRV
  EMU -- "http://10.0.2.2:8000" --> SRV
  CAM -. camera giả lập .-> EMU
```

| Cách | App gọi | Khi nào dùng |
|---|---|---|
| **A. Máy giả lập trên chính laptop** (chính) | `http://10.0.2.2:8000` (địa chỉ đặc biệt trỏ về laptop) | Luôn chạy được, không cần mạng |
| B. Điện thoại thật cùng mạng | `http://<IP-laptop>:8000` | Có điện thoại cài được app; nên phát hotspot từ điện thoại để không phụ thuộc Wi-Fi phòng |
| C. Tunnel HTTPS | `https://<tên>.trycloudflare.com` | Mạng chặn các máy nhìn thấy nhau |

## 2. Chạy server trên laptop trình bày

### 2a. Bằng Docker (cách chính, [ADR-017](adr/docker-server.md))

Một lần, trước buổi trình bày (cần Internet để tải image nền và thư viện, khoảng 1 GB):

1. Cài **Docker Desktop** (Windows: bật ảo hóa trong BIOS; Docker Desktop tự cài WSL2). Mở Docker Desktop, đợi biểu tượng cá voi báo "running".
2. `git clone https://github.com/thinhlai06/project-AI.git`, vào thư mục repo (đường dẫn ngắn như `D:\MediCheck` cho đỡ rắc rối).
3. Build và chạy:
   ```powershell
   docker compose up --build -d
   ```
4. Kiểm: mở `http://localhost:8000/health` → `{"ok": true, "model_version": "final-2026-11-08"}`; `docker ps` phải ghi `(healthy)`.
5. Lần đầu Windows hỏi tường lửa: chọn **Private networks**.

Hằng ngày: `docker compose up -d` (bật), `docker compose down` (tắt), `docker compose logs -f` (xem log). `restart: unless-stopped` nên mở Docker Desktop là server tự lên.

Đổi số luồng CPU: sửa `MEDICHECK_THREADS` trong `docker-compose.yml` (bằng số nhân thật của laptop), rồi `docker compose up -d`.

Không cần GPU. Sau khi build xong, chạy **không cần Internet**.

### 2b. Bằng Python venv (dự phòng khi Docker không chạy được)

1. Cài Python 64-bit 3.10–3.13 (khuyên 3.12), tick "Add python.exe to PATH". Python 3.14 chưa dùng được.
2. Repo ở đường dẫn ngắn (Windows giới hạn độ dài đường dẫn, `pip` lỗi nếu lồng sâu).
3. ```powershell
   py -3.12 -m venv .venv
   .venv\Scripts\python.exe -m pip install -r backendequirements.txt
   .venv\Scripts\python.exe -m uvicorn backend.medicheck_server.app:app --host 0.0.0.0 --port 8000
   ```

## 3. Máy giả lập Android

- Android Studio → Device Manager → tạo máy Pixel, Android 14 (API 34), có Google Play (để cài giọng tiếng Việt).
- **Camera:** Advanced settings → Back camera = `Webcam0` (dùng webcam laptop để chụp thuốc trên tay thật).
- **Ảnh có sẵn (đơn và thuốc):** kéo thả file ảnh hoặc PDF vào cửa sổ máy giả lập, file vào thư mục Download; app chọn bằng bộ chọn file/ảnh của Android (Files, Photos). Hoặc dùng `adb push anh.jpg /sdcard/Download/`. Ảnh muốn hiện trong Photos thì đẩy vào `/sdcard/Pictures/` rồi mở lại Photos. Không cần quyền đặc biệt trong app vì bộ chọn của hệ thống cấp quyền cho từng file.
- **Giọng nói:** Settings → System → Languages → Text-to-speech → Google → cài giọng Tiếng Việt.
- **Cleartext HTTP:** bản debug cho phép HTTP tới `10.0.2.2` và mạng nội bộ (cấu hình trong `android/app/src/main/res/xml/network_security_config.xml`).

## 4. Điện thoại thật (tùy chọn)

- Lấy IP laptop: `ipconfig` → dòng IPv4 của card Wi-Fi (ví dụ `192.168.43.10` khi nối hotspot).
- Trong app: Cài đặt → Địa chỉ server → `http://192.168.43.10:8000` → "Kiểm tra kết nối".
- iPhone: cần build bằng Xcode trên máy Mac ([ADR-002](adr/flutter-android-first.md)); app phải khai báo `NSLocalNetworkUsageDescription` và `NSAllowsLocalNetworking`.

## 5. Tunnel HTTPS (dự phòng)

```powershell
cloudflared tunnel --url http://localhost:8000
```

Lệnh in ra một địa chỉ `https://….trycloudflare.com`, dán vào Cài đặt của app. Cách này miễn phí và không cần tài khoản, nhưng **ảnh đi qua máy chủ Cloudflare**: chỉ dùng với dữ liệu mẫu VAIPE.

## 6. Checklist trước buổi trình bày

- [ ] `docker compose up --build` chạy được trên **chính laptop trình bày**, `docker ps` báo `healthy` (làm ở nhà, không để đến ngày trình bày).
- [ ] Đo trên chính laptop đó: `/health` OK; đọc đơn mẫu ≤ 10 giây; kiểm cữ 4 viên ≤ 3 giây (cổng 22/11).
- [ ] Chạy trọn kịch bản demo ([../quality/test-plan.md](../quality/test-plan.md) mục 5) trên máy giả lập.
- [ ] Giọng tiếng Việt đọc được trên máy giả lập.
- [ ] Đã thử cách B hoặc C ở mạng giống nơi trình bày (nếu dùng điện thoại thật).
- [ ] Sạc đầy laptop; tắt cập nhật Windows và chế độ ngủ.
- [ ] Có bản quay màn hình kịch bản demo làm phương án cuối.

## 7. Sự cố hay gặp

| Triệu chứng | Cách xử lý |
|---|---|
| `port 8000` đang dùng | Tắt server cũ (`docker compose down`, hoặc cửa sổ uvicorn), hoặc đổi `"8001:8000"` trong `docker-compose.yml` và đổi địa chỉ trong app |
| `docker compose` báo không kết nối được daemon | Mở Docker Desktop, đợi "running"; nếu vẫn lỗi, bật ảo hóa trong BIOS hoặc dùng cách 2b |
| Laptop chậm khi chạy cả Docker và máy giả lập | Tạo `%UserProfile%\.wslconfig` với `[wsl2]` và `memory=4GB`, rồi `wsl --shutdown` |
| App báo "Chưa kết nối được" | Mở `http://<địa chỉ>/health` bằng trình duyệt trên cùng thiết bị; kiểm tường lửa; dùng hotspot |
| Tên thuốc có dấu bị hỏng | Payload phải là UTF-8 (xem `backend/API.md`, ví dụ curl) |
| `pip` lỗi "No such file" | Đường dẫn quá dài: chuyển repo về `D:\MediCheck` |
| Kiểm thuốc chậm | Đặt `MEDICHECK_THREADS` bằng số nhân CPU thật; đóng ứng dụng nặng khác |
