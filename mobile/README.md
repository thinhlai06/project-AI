# MediCheck VN mobile

App Flutter MediCheck VN (xem docs/README.md ở thư mục gốc repo).

## Phiên bản khóa

Flutter 3.50.0 (stable) và Dart 3.14.0, cài ở `D:/flutter`; `pubspec.lock` được commit.

## Môi trường (Windows)

- Thêm `D:/flutter/bin` vào PATH người dùng.
- Đặt biến `PUB_CACHE=D:/flutter_pub_cache`.
- JDK dùng là JetBrains Runtime của Android Studio ở `D:/androistudio/jbr` (Flutter đã cấu hình).
- Android SDK ở `%LOCALAPPDATA%/Android/Sdk`.
- Mở terminal mới sau khi đổi biến môi trường.
- Giấy phép Android đã chấp nhận.

## Lệnh

Chạy trong thư mục mobile/:

- `flutter pub get`
- `flutter analyze`
- `flutter test`
- `flutter run`
- `dart run build_runner build --delete-conflicting-outputs` sau khi sửa bảng drift.

## Gói (khóa bởi pubspec.lock)

| Gói | Phiên bản | Ghi chú |
| --- | --- | --- |
| flutter_riverpod | 3.5.0 | |
| go_router | 18.1.4 | |
| drift | 2.35.4 | |
| drift_flutter | 0.3.1 | |
| http | 1.6.0 | |
| image | 4.13.1 | |
| camera | 0.12.2 | |
| file_picker | 13.3.3 | |
| flutter_local_notifications | 23.0.2 | |
| timezone | 0.11.2 | |
| flutter_timezone | 5.1.1 | |
| flutter_tts | 4.2.5 | |
| share_plus | 13.3.1 | |
| path_provider | 2.1.6 | |
| drift_dev | 2.35.3 | dev |
| build_runner | 2.17.1 | dev |
| flutter_lints | 6.0.0 | dev |
| material_ui | 1.11.0 | từ template Flutter 3.50, ADR-019 |

Không thêm gói ngoài ADR-015 khi chưa có ADR mới (AGENTS.md).

## Quyết định về file sinh ra

File sinh ra bởi drift/build_runner (`*.g.dart`) được commit, vì máy demo chỉ cần `flutter pub get` mà không cần chạy `build_runner`. Thư mục `build/` và `.dart_tool/` không bao giờ commit. Khi sửa bảng drift phải chạy lại `build_runner` và commit file sinh ra.

## applicationId

`vn.medicheck.mobile`; tên gói Dart là `mobile`.

## Rủi ro đã biết

`flutter_tts` áp dụng Kotlin Gradle Plugin; bản Flutter sau có thể không build được: theo dõi khi nâng cấp.

## Cấu hình Android (ST-01.2)

- `minSdk 29` (quyết định dự án NFR-08) và `compileSdk 37` (vì `flutter_local_notifications` 23 đòi).
- Core library desugaring: `desugar_jdk_libs 2.1.4`, bắt buộc với `flutter_local_notifications`; bật `isCoreLibraryDesugaringEnabled = true` trong `compileOptions`.
- Quyền khai báo và lý do:
  - `INTERNET`: bản release cần để gọi server AI (template chỉ khai ở debug/profile).
  - `CAMERA`: chụp ảnh đơn thuốc và viên thuốc.
  - `POST_NOTIFICATIONS`: hiện thông báo nhắc uống thuốc (Android 13+).
  - `RECEIVE_BOOT_COMPLETED`: khôi phục lịch nhắc sau khi khởi động lại máy.
  - `USE_EXACT_ALARM`: báo thức chính xác cho cữ thuốc, tự cấp; nhưng chính sách Google Play dành cho app báo thức/lịch nên có rủi ro nếu phát hành.
- Quyền đã gỡ (do plugin camera gộp vào, app không dùng): `RECORD_AUDIO`, `READ_EXTERNAL_STORAGE` (dùng `tools:node="remove"`).
- Cleartext (HTTP) chỉ ở bản debug: file `android/app/src/debug/res/xml/network_security_config.xml`; bản release không có file này và chặn HTTP theo mặc định.
- Nhãn app: `MediCheck`.
- Lần build đầu mất 5-8 phút và Gradle tự tải thêm thành phần Android SDK.
- Nếu gặp lỗi Kotlin "Could not close incremental caches", thêm `kotlin.incremental=false` vào `android/gradle.properties`.