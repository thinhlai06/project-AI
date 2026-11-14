# ADR-006: Detector YOLO26s nhánh NMS

- **Trạng thái:** Đã chấp nhận
- **Ngày:** 2026-11-08
- **Người quyết:** phụ trách AI

## Bối cảnh

Cần tìm mọi viên rời trong ảnh lòng bàn tay, chạy nhanh trên CPU laptop.

## Quyết định

**YOLO26s** (Ultralytics 8.4.204), 1 lớp, ảnh 640, nhánh **NMS**, ngưỡng tin cậy 0,5. Train trên VAIPE nhãn v3 (box chặt) + ảnh nền trống + 3.051 ảnh ngoài (A/B D2-B). App chỉ đếm viên có tâm trong khung chụp.

## Phương án đã cân nhắc

| Phương án | Vì sao không chọn |
|---|---|
| YOLO11s | YOLO26s hơn về mAP và tốc độ CPU theo công bố của Ultralytics |
| Nhánh end-to-end (không NMS) của YOLO26 | Kém ~4 điểm "đếm đúng số viên" trên val |
| Bản n (nhỏ hơn) / m (lớn hơn) | Bản s đã chạm trần trên val (đếm đúng 98,6%); không cần lớn hơn |

## Hệ quả

- Đếm đúng 98,5% cảnh test; ~120–140 ms mỗi ảnh trên CPU.
- Giấy phép AGPL-3.0: phát hành dịch vụ phải công khai mã nguồn backend.
