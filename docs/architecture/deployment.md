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
   .venv\Scripts\python.exe -m pip install -r backend\requirements.txt
   .venv\Scripts\python.exe -m uvicorn backend.medicheck_server.app:app --host 0.0.0.0 --port 8000
   ```

## 3. Máy giả lập Android

Dùng AVD có sẵn `pixel_7_-_api_36_0` (API 36, ảnh Google Play để cài giọng tiếng Việt, 1536 MB RAM): API 36 thỏa yêu cầu "API 34 trở lên". Không dùng `Medium_Phone_API_37.0`: chưa chạy lần nào và sẽ chiếm thêm khoảng 10 GB ở ổ C. AVD này là AVD có sẵn của chủ máy nên chỉ chạy ở chế độ `-no-snapshot -read-only` (không nạp và không lưu snapshot, mọi thay đổi bị bỏ khi tắt) và phải gỡ app sau khi thử; `config.ini` và `snapshots/` đã kiểm là không đổi (2026-11-16). Không sửa `config.ini` của AVD.

Build APK debug bằng `flutter build apk --debug` (chạy trong `mobile/`; đặt `GRADLE_USER_HOME=D:/gradle_home` và `PUB_CACHE=D:/flutter_pub_cache` cho tiến trình build, thiếu thì Gradle tạo bản cache thứ hai ở ổ C). APK debug đo được 188 MB.

Các lệnh `adb`/`emulator` đã chạy thật ngày 2026-11-16; hàm `Get-OurSerial` và các dòng `throw` mới thêm sau review vòng 2, đã thử riêng hàm với dữ liệu giả, chưa chạy lại cả khối trên emulator (PowerShell, đường dẫn viết bằng dấu `/`; `adb` không có trong PATH nên gọi bằng `$adb`, luôn kèm `-s <serial>` với serial do hàm `Get-OurSerial` trả về, không ghim cứng). Kiểm số emulator trước và sau khi mở:

```powershell
$sdk = "$env:LOCALAPPDATA/Android/Sdk"
$adb = "$sdk/platform-tools/adb.exe"
# Hàm kiểm: trả về serial CHỈ KHI có đúng MỘT dòng emulator-*, nó ở trạng thái device và tiến trình $p của ta còn sống; ngược lại trả $null
function Get-OurSerial {
  $all = @(& $adb devices | Select-String '^emulator-\d+')
  if ($p.HasExited -or $all.Count -ne 1 -or $all[0].Line -notmatch '\sdevice\s*$') { return $null }
  return ($all[0].Line -split '\s+')[0]
}
# (a) TRƯỚC khi mở: không được có dòng emulator-* nào. Có (AVD của chủ máy, Android Studio, dự án khác) → DỪNG, hỏi chủ máy (ai-workflow mục 7); không kill, không dùng lại.
if (@(& $adb devices | Select-String '^emulator-\d+').Count -gt 0) { throw "Đã có emulator đang chạy: dừng và hỏi chủ máy" }
# (b) mở emulator, giữ tiến trình trong $p
$p = Start-Process "$sdk/emulator/emulator.exe" -ArgumentList '-avd','pixel_7_-_api_36_0','-no-snapshot','-read-only','-no-audio','-no-boot-anim' -PassThru   # giữ lại PID
# (c) đợi (khoảng 30 s) tới khi Get-OurSerial trả về serial; quá 3 phút vẫn $null thì DỪNG, hỏi chủ máy, không chạy lệnh nào dùng serial
$deadline = (Get-Date).AddMinutes(3)
do { Start-Sleep 5; $serial = Get-OurSerial } until ($serial -or $p.HasExited -or (Get-Date) -gt $deadline)
if (-not $serial) { throw "Không có đúng một emulator của mình: dừng và hỏi chủ máy" }
& $adb -s $serial shell getprop sys.boot_completed      # lặp tới khi in ra 1
# (d) kiểm lại bằng `if ((Get-OurSerial) -ne $serial) { throw "emulator đổi: dừng" }` trước các lệnh ghi (install, uninstall) và trước emu kill (có dòng kiểm sẵn ở dưới); các lệnh còn lại đã kèm -s $serial
# cài APK debug đã build; đường dẫn tính từ thư mục gốc repo
if ((Get-OurSerial) -ne $serial) { throw "emulator đổi: dừng" }
& $adb -s $serial install -r mobile/build/app/outputs/flutter-apk/app-debug.apk
& $adb -s $serial shell am start -n vn.medicheck.mobile/.MainActivity
& $adb -s $serial shell screencap -p /sdcard/medicheck_evidence.png
& $adb -s $serial pull /sdcard/medicheck_evidence.png "<đường dẫn đích>"
& $adb -s $serial shell rm /sdcard/medicheck_evidence.png   # xóa ảnh trên máy ảo sau khi pull
& $adb -s $serial logcat -d -s flutter:V AndroidRuntime:E
if ((Get-OurSerial) -ne $serial) { throw "emulator đổi: dừng" }
& $adb -s $serial uninstall vn.medicheck.mobile   # gỡ app sau khi thử
if ((Get-OurSerial) -ne $serial) { throw "emulator đổi: dừng" }
& $adb -s $serial emu kill   # (e) chỉ emu kill máy mình đã mở (PID trong $p); không bao giờ kill emulator không phải do mình mở
```

Đã thử hàm `Get-OurSerial` với dữ liệu `adb devices` giả: 0 dòng, 2 dòng, `offline`, `unauthorized`, tiến trình đã thoát đều trả rỗng; điện thoại thật cùng emulator thì chỉ đếm emulator. Còn lại một khe hở: chủ máy mở emulator của họ đúng lúc emulator của ta không lên; hàm chặn được (tiến trình `$p` đã thoát) nhưng nếu muốn chắc hơn thì mở với `-port 5580` để serial là `emulator-5580` (chưa thử).

- Serial lấy từ hàm, không bao giờ gõ tay.
- Nếu (a), (c) hay bước kiểm lại trước `uninstall`/`emu kill` thất bại: DỪNG, hỏi chủ máy, không làm gì thêm.
- Bỏ lệnh `emu avd name`: AVD của chủ máy cũng cùng tên `pixel_7_-_api_36_0` nên lệnh đó không phân biệt được emulator của mình với emulator của chủ máy.
- Emulator không lên sau khoảng 3 phút → dừng và hỏi chủ dự án (ai-workflow mục 4b, mục 7).

Không dùng `adb kill-server` (adb dùng chung với IDE khác) và không chạy `wsl --shutdown` trên máy dev dùng chung. Không dán output `logcat` vào nhật ký hay PR nếu nó có thể chứa chữ từ đơn thuốc (BR-10).

- **Camera:** máy dev không có webcam nào nhìn thấy từ máy giả lập (`emulator -webcam-list` rỗng) nên Back camera giữ `virtualscene` (mặc định của AVD). Máy nào có webcam thì thêm cờ `-camera-back webcam0` khi mở emulator để chụp thuốc trên tay thật; kiểm webcam thật làm ở ST-12.1/ST-25.3.
- **Kết quả đo (2026-11-16):** emulator khởi động trong 30 s; trang kiểm kết nối tạm hiện "Đã kết nối (final-2026-11-08)" qua `http://10.0.2.2:8000` (cleartext chạy được ở bản debug). Tắt container server rồi bấm nút thì hiện "Chưa kết nối được" (không bao giờ hiện chữ thành công); bật lại server thì kết nối lại bình thường.
- **Ảnh có sẵn (đơn và thuốc):** kéo thả file ảnh hoặc PDF vào cửa sổ máy giả lập, file vào thư mục Download; app chọn bằng bộ chọn file/ảnh của Android (Files, Photos). Hoặc dùng `adb push anh.jpg /sdcard/Download/`. Ảnh muốn hiện trong Photos thì đẩy vào `/sdcard/Pictures/` rồi mở lại Photos. Không cần quyền đặc biệt trong app vì bộ chọn của hệ thống cấp quyền cho từng file.
- **Giọng nói:** Settings → System → Languages → Text-to-speech → Google → cài giọng Tiếng Việt.
- **Cleartext HTTP:** bản debug cho phép HTTP tới mọi host (gồm `10.0.2.2` và IP laptop trong mạng nội bộ; cấu hình trong `mobile/android/app/src/debug/res/xml/network_security_config.xml`), chỉ có ở bản debug; bản release chặn HTTP mặc định (ST-01.2).

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
| Laptop chậm khi chạy cả Docker và máy giả lập | `%UserProfile%\.wslconfig` với `[wsl2]` và `memory=4GB`: nếu chưa có thì tạo, còn có thì gộp mục `[wsl2]`; lưu việc trước vì `wsl --shutdown` tắt mọi distro và cả Docker Desktop, rồi mở lại Docker Desktop (chỉ áp dụng cho laptop trình bày; trên máy dev dùng chung thì KHÔNG làm, hỏi chủ máy) |
| App báo "Chưa kết nối được" | Mở `http://<địa chỉ>/health` bằng trình duyệt trên cùng thiết bị; kiểm tường lửa; dùng hotspot |
| Tên thuốc có dấu bị hỏng | Payload phải là UTF-8 (xem `backend/API.md`, ví dụ curl) |
| `pip` lỗi "No such file" | Đường dẫn quá dài: chuyển repo về `D:\MediCheck` |
| Kiểm thuốc chậm | Đặt `MEDICHECK_THREADS` bằng số nhân CPU thật; đóng ứng dụng nặng khác |
