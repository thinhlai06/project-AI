# ADR-007: Bộ nhận dạng DINOv3 ViT-S/16

- **Trạng thái:** Đã chấp nhận
- **Ngày:** 2026-11-08
- **Người quyết:** phụ trách AI

## Bối cảnh

Viên thuốc giống nhau nhiều, màu không ổn định theo ánh sáng; dữ liệu ít ở nhiều lớp; phải chạy CPU.

## Quyết định

**DINOv3 ViT-S/16** (token CLS), ảnh 384, crop nguồn 512 lề 13%, đầu cosine 107 lớp. Huấn luyện 2 giai đoạn: đóng băng, rồi mở toàn bộ backbone với LLRD 0,75; loss cosine softmax + loss 107 có điều kiện theo đơn; lấy checkpoint cuối; seed 1 (A/B R3-B).

## Phương án đã cân nhắc

| Phương án | Vì sao không chọn |
|---|---|
| DINOv2-S | Đóng băng kém DINOv3 9,4 điểm báo xanh; fine-tune trượt chuẩn an toàn |
| EfficientNet-B0 (CNN) | Kém 6,6 điểm báo xanh cùng giao thức; giữ làm mốc so sánh |
| CosFace | Thua cosine softmax ở A/B R2-B |
| Ảnh 448 | Hòa khi chạy cả chuỗi, chậm hơn |
| TTA / ghép nhiều mô hình | TTA +0,7 điểm nhưng chậm 8 lần; ghép mô hình không hơn |

## Hệ quả

- Nhận đúng trong ứng viên 95,8% (val); ~170–190 ms mỗi viên trên CPU.
- DINOv3 License (Meta, không phải OSI): phân phối phải kèm giấy phép, công bố phải ghi nhận DINOv3.
