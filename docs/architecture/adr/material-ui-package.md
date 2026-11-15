# ADR-019: Dùng gói material_ui (thành phần Material của Flutter 3.50)

- **Trạng thái:** Đã chấp nhận
- **Ngày:** 2026-11-15
- **Người quyết:** chủ dự án
- **Liên quan:** [ADR-015](flutter-app-stack.md) (bộ thư viện app)

## Bối cảnh

Flutter 3.50 tách thành phần Material thành gói `material_ui`: template `flutter create` đã khai báo `material_ui` trong `pubspec.yaml` và import `package:material_ui/material_ui.dart`. `package:flutter/material.dart` bị deprecated nên `flutter analyze` không sạch nếu dùng, mà "analyze sạch" là gate của AGENTS.md. ADR-015 không liệt kê gói này; AGENTS.md cấm thêm thư viện ngoài ADR-015 khi chưa có ADR mới.

## Quyết định

- Cho phép `material_ui` (khai báo `^1.1.0`, khóa 1.11.0 bởi `pubspec.lock`) như một phần của framework, thay cho `flutter/material.dart`.
- Bỏ `cupertino_icons` (không dùng).
- Các phụ thuộc gián tiếp do `drift_flutter` kéo vào `pubspec.lock` (gồm hai gói rỗng đã hết hạn `sqlite3_flutter_libs`, `sqlcipher_flutter_libs`) không phải thư viện thêm vào `pubspec.yaml` và không cần ADR riêng.

## Phương án đã cân nhắc

| Phương án | Vì sao không chọn |
|---|---|
| Dùng `package:flutter/material.dart` | Deprecated, `flutter analyze` không sạch (gate của AGENTS.md) |
| Tự tắt cảnh báo trong `analysis_options.yaml` | Che dấu vấn đề, nâng cấp Flutter sẽ gãy |

## Hệ quả

- Mọi màn dùng `package:material_ui/material_ui.dart`.
- Không thêm gói UI khác.
- Khi Flutter đổi lại thì viết ADR mới.
