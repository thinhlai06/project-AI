# Những gì đã cài hoặc tạo trên máy khi làm dự án

> **Trả lời câu hỏi:** khi làm app, các phiên AI (Claude Code, subagent, Qoder) đã cài hoặc tạo gì ngoài thư mục repo, vì sao cần, và gỡ thế nào khi không dùng nữa.
> Cập nhật: 2026-11-16 · Đường dẫn viết bằng `%USERPROFILE%`, `%LOCALAPPDATA%` và dấu `/`. File này là danh sách **chung** cho mọi máy; bản kiểm kê đầy đủ của từng máy (đường dẫn thật, dung lượng, việc đã dọn, đồ của các phiên AI trước) giữ cục bộ, không commit.

## 1. Cài hoặc tạo khi làm app Flutter

| Thứ | Ở đâu | Dung lượng | Vì sao cần | Còn cần? | Gỡ thế nào |
|---|---|---|---|---|---|
| Flutter SDK 3.50.0 (stable) | `D:/flutter` | 1,5 GB | Dựng và chạy app `mobile/` | Có | Xóa thư mục; bỏ `D:/flutter/bin` khỏi PATH người dùng |
| Pub cache | `D:/flutter_pub_cache` (biến `PUB_CACHE`) | 0,3 GB | Gói Dart của app | Có | Xóa thư mục và biến `PUB_CACHE` |
| Gradle home | `D:/gradle_home` (biến `GRADLE_USER_HOME`) | 3,5 GB, sẽ phình thêm | Gradle 9.5.0 và cache build | Có | Xóa thư mục (tải lại khi build); bỏ biến `GRADLE_USER_HOME` |
| Android platform 35 | `%LOCALAPPDATA%/Android/Sdk/platforms/android-35` | 0,1 GB | Thư viện `jni`, `jni_flutter` (qua `path_provider`) và `flutter_timezone` biên dịch với compileSdk 35 | Có, khi còn các gói đó | Xóa thư mục hoặc `sdkmanager --uninstall "platforms;android-35"`; build sau tự cài lại |
| Android platform 36 | `Sdk/platforms/android-36` | 0,1 GB | `flutter_tts` biên dịch với compileSdk 36 | Có | như trên |
| Android platform 37 | `Sdk/platforms/android-37.0` | 0,1 GB | compileSdk của app (`flutter_local_notifications` 23 đòi 37); có sẵn từ Android Studio | Có | không gỡ |
| CMake 3.22.1 | `Sdk/cmake/3.22.1` | 0,04 GB | Biên dịch `libdartjni.so` của thư viện `jni` | Có, khi còn `path_provider` | như trên |
| NDK 28.2.13676358 | `Sdk/ndk/28.2.13676358` (có thể là junction sang ổ khác) | 2,1 GB | Biên dịch mã gốc `libdartjni.so` | Có, khi còn `path_provider` | **Đừng gỡ bằng SDK Manager khi đang là junction** (có thể xóa cả dữ liệu đích); gỡ thì xóa liên kết trước. Build sau tự tải lại 2 GB |
| Khóa ký debug | `%USERPROFILE%/.android/debug.keystore` | nhỏ | Ký APK debug, do build debug đầu tiên tạo | Có | Xóa; tự tạo lại |
| Kết quả build trong repo | `mobile/build`, `mobile/.dart_tool`, `mobile/android/.gradle` | ~1 GB | Đầu ra build | Không | `flutter clean`; không commit (đã bị `.gitignore` bỏ qua) |
| Image và container Docker của server AI | image `medicheck-server:latest` (~1,5 GB), container `projectai-medicheck-server-1`; dữ liệu nằm trong ổ ảo của Docker Desktop | ~1,5 GB | Chạy server AI (ADR-017) | Có, khi demo | `docker compose down --rmi local` |

Ghi chú: ba biến môi trường người dùng `PATH` (có `D:/flutter/bin`), `PUB_CACHE`, `GRADLE_USER_HOME` đặt ở mức User. Một phiên Claude Code đang chạy không thấy biến mới đặt: phải mở phiên mới, hoặc đặt biến cho từng tiến trình (nếu thiếu `GRADLE_USER_HOME`, Gradle tạo thư mục trùng ở ổ C).


## 2. Vì sao lần dựng thử đã cài thêm (câu hỏi của chủ dự án)

Lần build đầu của app cần một số thành phần Android mà máy chưa có, nên Gradle tự tải và cài (giấy phép đã chấp nhận từ trước nên không hỏi): platform 35 và 36, CMake 3.22.1 và NDK 28.2. Chúng **cần thật**: thư viện `jni` (đi kèm `path_provider`) phải biên dịch mã gốc bằng NDK và CMake, và vài thư viện biên dịch với compileSdk 35 hoặc 36. Chúng nhỏ (trừ NDK 2,1 GB, đã chuyển sang ổ D). Phần **lãng phí thật** là bản Gradle thứ hai ở ổ C (6,3 GB) và các thư mục thử build (3,3 GB): đã xóa. Nếu sau này bỏ `path_provider` thì NDK, CMake và platform 35 không còn cần.


## 3. Luật từ nay (đề xuất, ghi ở `docs/process/ai-workflow.md`)

- Mọi thứ cài hoặc tải ngoài thư mục repo phải được ghi vào file này trong cùng PR.
- Subagent và Qoder phải đặt `GRADLE_USER_HOME=D:/gradle_home` và `PUB_CACHE=D:/flutter_pub_cache` cho tiến trình khi chạy `flutter` hoặc `gradle`; thư mục thử nghiệm (dự án thử, clone tạm) phải nằm ở ổ D (`D:/project AI_tmp/`) hoặc bị xóa ngay khi xong.
- Không dựng thử bằng cách cài thêm vào hệ thống khi không cần; nếu bắt buộc, ghi lại ở đây.
- Thiết bị ảo (AVD) có sẵn của chủ máy chỉ được chạy ở chế độ `-no-snapshot -read-only` và phải gỡ app sau khi thử.
