# Triển khai và chạy demo

> **Trả lời câu hỏi:** chạy server ở đâu, app nối vào bằng cách nào, trước buổi trình bày cần kiểm gì.
> Quyết định: [ADR-004](adr/laptop-demo-server.md) (laptop làm server, không Docker, không cloud).
> Cập nhật: 2026-11-15 · Trạng thái: **đã chốt**

## 1. Bố trí

```mermaid
flowchart LR
  subgraph Laptop trình bày [Laptop trình bày (Windows)]
    SRV[Server AI<br/>uvicorn :8000]
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

## 2. Cài server trên laptop trình bày (một lần)

1. Cài Python 64-bit 3.10–3.13 (khuyên 3.12), tick "Add python.exe to PATH". Python 3.14 chưa dùng được.
2. Lấy repo (`git clone` hoặc tải zip từ GitHub) vào đường dẫn ngắn, ví dụ `D:\MediCheck`. Windows giới hạn độ dài đường dẫn, nên thư mục lồng sâu sẽ làm `pip` lỗi.
3. Mở PowerShell tại thư mục repo:
   ```powershell
   py -3.12 -m venv .venv
   .venv\Scripts\python.exe -m pip install -r backend\requirements.txt
   ```
4. Chạy server:
   ```powershell
   .venv\Scripts\python.exe -m uvicorn backend.medicheck_server.app:app --host 0.0.0.0 --port 8000
   ```
5. Mở `http://localhost:8000/health` → phải thấy `{"ok": true, "model_version": "final-2026-11-08"}`.
6. Lần đầu Windows hỏi tường lửa: chọn **Private networks**.

Không cần GPU, không cần Docker, không cần Internet khi chạy (chỉ cần lúc cài).

## 3. Máy giả lập Android

- Android Studio → Device Manager → tạo máy Pixel, Android 14 (API 34), có Google Play (để cài giọng tiếng Việt).
- **Camera:** Advanced settings → Back camera = `Webcam0` (dùng webcam laptop để chụp thuốc trên tay thật).
- **Ảnh mẫu:** kéo thả file ảnh vào cửa sổ máy giả lập để đưa vào thư viện ảnh, hoặc dùng "Thử với đơn mẫu".
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

- [ ] Đo trên **chính laptop trình bày**: `/health` OK; đọc đơn mẫu ≤ 10 giây; kiểm cữ 4 viên ≤ 3 giây (cổng 22/11).
- [ ] Chạy trọn kịch bản demo ([../quality/test-plan.md](../quality/test-plan.md) mục 5) trên máy giả lập.
- [ ] Giọng tiếng Việt đọc được trên máy giả lập.
- [ ] Đã thử cách B hoặc C ở mạng giống nơi trình bày (nếu dùng điện thoại thật).
- [ ] Sạc đầy laptop; tắt cập nhật Windows và chế độ ngủ.
- [ ] Có bản quay màn hình kịch bản demo làm phương án cuối.

## 7. Sự cố hay gặp

| Triệu chứng | Cách xử lý |
|---|---|
| `port 8000` đang dùng | Tắt cửa sổ server cũ, hoặc chạy `--port 8001` và đổi địa chỉ trong app |
| App báo "Chưa kết nối được" | Mở `http://<địa chỉ>/health` bằng trình duyệt trên cùng thiết bị; kiểm tường lửa; dùng hotspot |
| Tên thuốc có dấu bị hỏng | Payload phải là UTF-8 (xem `backend/API.md`, ví dụ curl) |
| `pip` lỗi "No such file" | Đường dẫn quá dài: chuyển repo về `D:\MediCheck` |
| Kiểm thuốc chậm | Đặt `MEDICHECK_THREADS` bằng số nhân CPU thật; đóng ứng dụng nặng khác |
