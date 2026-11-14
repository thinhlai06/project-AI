# ADR-001: Suy luận trên server, app không chạy mô hình

- **Trạng thái:** Đã chấp nhận
- **Ngày:** 2026-11-08
- **Người quyết:** phụ trách AI

## Bối cảnh

Kiểm thuốc cần 2 mô hình (detector 36 MB, nhận dạng 83 MB) cộng logic ghép và ngưỡng đã được đo an toàn; đọc đơn cần thêm 2 mô hình OCR. Nhóm có 2 người làm mobile và 6 tuần. Con số an toàn (≤ 2%) chỉ đúng khi tiền xử lý giống hệt lúc đo.

## Quyết định

Mọi mô hình chạy trên server Python (ONNX Runtime CPU). App chỉ chụp, chuẩn bị ảnh, gửi lên và hiển thị. Logic an toàn chỉ có **một** bản, trong `backend/medicheck_server/infer.py`.

## Phương án đã cân nhắc

| Phương án | Vì sao không chọn |
|---|---|
| Chạy mô hình trên điện thoại (ONNX Runtime Mobile / TFLite) | Phải viết lại tiền xử lý, ghép, ngưỡng bằng Dart và đo lại an toàn; app nặng thêm ~300 MB; không kịp hạn |
| Gọi API AI thuê ngoài (VLM) | Tốn tiền, gửi dữ liệu y tế ra ngoài, nguy cơ bịa liều, không đo được an toàn |

## Hệ quả

- Server đã kiểm khớp từng bước với lúc đo (1.244/1.244 cảnh val cùng kết luận).
- App cần mạng để đọc đơn và kiểm thuốc; nhắc lịch vẫn chạy khi mất mạng.
- Cần một máy chạy server khi demo ([ADR-004](laptop-demo-server.md)).
- Xem lại khi: cần dùng ngoài phạm vi demo, hoặc có thời gian làm bản chạy trên máy (giai đoạn 2).
