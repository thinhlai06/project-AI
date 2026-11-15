# ADR-018: Ảnh viên cắt chỉ nằm trong bộ nhớ, thay ảnh mẫu từ VAIPE

- **Trạng thái:** Đã chấp nhận
- **Ngày:** 2026-11-15
- **Người quyết:** chủ dự án
- **Liên quan:** [ADR-016](prescription-image-on-device.md) (vẫn giữ: không lưu ảnh thuốc)

## Bối cảnh

Yêu cầu cũ FR-DOSE-02 muốn hiện ảnh mẫu từng thuốc (lấy từ crop VAIPE) ở màn Cữ cần uống. Ảnh VAIPE không phản ánh viên thật của người dùng, dữ liệu đang kẹt, và ảnh mẫu không làm tăng độ an toàn. Server cắt viên để đưa vào DINOv3 nhưng **không trả ảnh cắt về**, chỉ trả `box` (0–1).

## Quyết định

- Bỏ FR-DOSE-02 và mọi ảnh mẫu dựng sẵn (ST-20, ST-00.3).
- Thay bằng FR-VER-11: ngay sau khi có kết quả, app **cắt từng viên từ ảnh vừa chụp** theo `pills[].box` và hiện danh sách "Thuốc theo kết quả": mỗi thuốc **một ảnh**, kèm tên, số viên, trạng thái.
- Ảnh cắt **chỉ nằm trong bộ nhớ** (`Uint8List`, `Image.memory`, provider `autoDispose`): không ghi đĩa, không vào database, không gửi đi đâu. Bỏ khi rời màn kết quả hoặc xong cữ; với chụp lại, giữ ảnh lượt 1 đến khi xong cữ.
- Ảnh cắt **chỉ để người dùng nhìn**: không tham gia quyết định xanh/đỏ/vàng, không có ô sửa tên hay số viên (BR-01, BR-13).
- Không cần sửa server.

## Phương án đã cân nhắc

| Phương án | Vì sao không chọn |
|---|---|
| Ảnh mẫu VAIPE dựng sẵn | Không phải viên thật của người dùng; dữ liệu kẹt; có thể gây hiểu nhầm khi hiệu thuốc khác hình |
| Lưu ảnh cắt để hiện ở cữ sau ("viên bác đã kiểm lần trước") | Phải lưu ảnh thuốc (đổi BR-10); báo xanh nhầm (≤ 2%) sẽ lưu nhầm và lặp lại; lần đầu vẫn không có ảnh. Chủ dự án chọn không lưu |
| Server trả ảnh cắt trong phản hồi | Tăng dung lượng phản hồi và đổi API chỉ để làm việc app tự làm được |

## Hệ quả

- BR-10 và ADR-016 không đổi: vẫn không lưu ảnh thuốc.
- Màn Cữ cần uống không có ảnh viên (không có gì để hiện trước lần chụp đầu).
- App cần `core/media/pill_crop.dart` và `core/domain/result_groups.dart` (story ST-29); test TC-20 đến TC-22.
- Tắt app giữa chừng thì mất ảnh cắt: chấp nhận được, kết quả cữ vẫn nằm trong lịch sử dạng chữ.
