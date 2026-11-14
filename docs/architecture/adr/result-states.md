# ADR-009: Ba trạng thái xanh/đỏ/vàng, không mô tả màu, không đoán

- **Trạng thái:** Đã chấp nhận
- **Ngày:** 2026-11-08 (bản đầu 2026-11-03)
- **Người quyết:** phụ trách AI, nhóm sản phẩm

## Quyết định

| Trạng thái | Khi nào | Ghi chú |
|---|---|---|
| Xanh | Khớp chắc thuốc của cữ, đúng số lượng | Cả cữ xanh chỉ khi số viên đúng và mọi viên xanh |
| Đỏ – cữ khác | Khớp chắc thuốc cữ khác của đơn (ngưỡng 0,0529) | Bắt 95,8% viên bị chuyển cữ, báo oan 0,22% (test) |
| Đỏ – ngoài đơn | Lớp ngoài đơn vượt rõ lớp trong đơn (ngưỡng 0,30) | Ngưỡng chặt để ít báo oan; vẫn 1,40% oan trên test |
| Vàng | Còn lại: chưa chắc, lệch số lượng, 14 lớp không đo được, viên của thuốc chỉ nhắc lịch | Luôn kèm "hãy kiểm vỏ hộp" |

- Đỏ và lời khuyên về ảnh **không bao giờ** biến cữ thành xanh, nên không ảnh hưởng con số an toàn.
- Không đoán "có thể là thuốc Z"; không mô tả màu viên (màu đổi theo đèn và máy).
- Viên của thuốc chỉ nhắc lịch không bao giờ bị đỏ "ngoài đơn".
- Chụp lại tối đa 1 lần; viên đã xanh giữ xanh; sau đó là "Tôi đã kiểm vỏ hộp".

## Phương án đã cân nhắc

| Phương án | Vì sao không chọn |
|---|---|
| Chỉ xanh/vàng, không đỏ | Lỗi hay gặp nhất là nhầm cữ; đỏ giúp người dùng bỏ đúng viên ra |
| Ngưỡng đỏ "ngoài đơn" = 0,0529 | 2,67% viên đúng bị báo đỏ oan; "Đừng uống" sai có thể làm bỏ liều |
| Chặn ảnh tối/mờ trước khi nhận dạng | Làm mất báo xanh mà không thêm an toàn; chỉ thêm lời khuyên |
