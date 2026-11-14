# ADR-015: Bộ thư viện app: Riverpod, go_router, drift, http

- **Trạng thái:** Đã chấp nhận (2026-11-15)
- **Ngày:** 2026-11-14
- **Người quyết:** phụ trách AI đề xuất, nhóm mobile duyệt

## Bối cảnh

App nhỏ (khoảng 14 màn), 2 người làm trong 6 tuần, có dùng AI agent để viết code. Cần một bộ thư viện phổ biến, nhiều tài liệu, để code do người và AI viết giống nhau.

## Quyết định

| Việc | Chọn |
|---|---|
| Trạng thái + phụ thuộc | `flutter_riverpod` (provider viết tay, không bắt buộc sinh code) |
| Điều hướng | `go_router` |
| Database | `drift` + `drift_flutter` (dev: `drift_dev`, `build_runner`) |
| HTTP | `http` |
| Ảnh | `image` v4 trong isolate |
| Camera / chọn file | `camera`, `file_picker` |
| Lưu file ảnh đơn | `path_provider` ([ADR-016](prescription-image-on-device.md)) |
| Nhắc | `flutter_local_notifications` + `timezone` + `flutter_timezone` |
| Giọng nói | `flutter_tts` |
| Chia sẻ | `share_plus`; ảnh phiếu đơn vẽ bằng `RepaintBoundary` của Flutter, không thêm gói PDF |
| Test | `flutter_test`, `flutter_lints` (có sẵn trong SDK) |
| Cấu trúc | feature-first; logic nghiệp vụ ở `lib/core/domain` bằng Dart thuần, có unit test |

Phiên bản cụ thể của Flutter và từng gói ghi trong `mobile/pubspec.yaml` lúc khởi tạo dự án, rồi khóa bằng `pubspec.lock`.

## Phương án đã cân nhắc

| Phương án | Vì sao không chọn |
|---|---|
| `provider` / `setState` | Khó test và khó tách logic khi app lớn dần |
| BLoC | Nhiều code khuôn mẫu hơn cho app cỡ này |
| `dio` | Không cần tính năng nào mà `http` thiếu; ví dụ sẵn có dùng `http` |

## Hệ quả

- Nhóm mobile cần học Riverpod cơ bản (provider, `ref.watch`, `AsyncValue`).
- Nếu nhóm đã quen bộ khác, đổi ADR này trước khi tạo dự án Flutter, không đổi giữa chừng.
