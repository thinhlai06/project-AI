# ADR-002: Flutter, demo chính trên máy giả lập Android, giữ đường iOS

- **Trạng thái:** Đã chấp nhận (2026-11-15)
- **Ngày:** 2026-11-14
- **Người quyết:** cả nhóm (người dùng chọn hướng máy giả lập 2026-11-14)

## Bối cảnh

Nhóm chỉ có iPhone, không có máy Android và không có máy Mac. Build app iOS bắt buộc phải có Xcode, mà Xcode chỉ chạy trên macOS. Máy giả lập Android chạy được trên laptop Windows.

## Quyết định

- Viết app bằng **Flutter**: một mã nguồn cho cả Android và iOS. Hai hướng **không** khác nhau về code; khác ở khâu build và cài.
- **Đích demo chính:** máy giả lập Android (API 34) trên laptop trình bày, dùng webcam laptop làm camera.
- **Giữ đường iOS mở:** chỉ dùng gói Flutter hỗ trợ cả hai nền tảng; khai báo sẵn quyền iOS (camera, thông báo, mạng nội bộ) trong `Info.plist`.
- **Đích phụ (nếu kịp):** cài lên iPhone thật bằng một trong hai cách, chọn sau khi app chạy ổn trên Android:
  1. mượn một máy Mac 1 buổi, build bằng Xcode với Apple ID miễn phí (app hết hạn sau 7 ngày, cài lại trước buổi trình bày);
  2. build trên dịch vụ CI có máy macOS (ví dụ Codemagic gói miễn phí) rồi cài qua công cụ ký bằng Apple ID trên Windows. Cách này nhiều bước và phụ thuộc công cụ bên thứ ba, phải thử trước.
- Phương án rẻ nhất để có thiết bị thật: mượn hoặc mua một điện thoại Android cũ.

## Phương án đã cân nhắc

| Phương án | Vì sao không chọn |
|---|---|
| Chỉ làm iOS | Không có máy Mac để build hằng ngày; không có máy giả lập iOS trên Windows |
| Web app (PWA) chạy trên Safari iPhone | Nhắc thuốc theo giờ trên web iOS rất hạn chế; camera cần HTTPS; khác hẳn kiến trúc app |
| React Native | Nhóm và tài liệu đã theo Flutter; không giải quyết được việc build iOS cần Mac |

## Hệ quả

- Phát triển và kiểm thử hằng ngày hoàn toàn trên Windows.
- Demo trên máy giả lập kém thuyết phục hơn điện thoại thật: bù bằng webcam (chụp thuốc trên tay thật) và chiếu màn hình máy giả lập.
- Mốc thử iOS nằm trong [roadmap](../../product/roadmap.md); nếu không mượn được Mac thì bỏ, không ảnh hưởng MVP.
