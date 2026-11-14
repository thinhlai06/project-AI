# ADR-008: Chuẩn an toàn ≤ 2% và tập test dùng một lần

- **Trạng thái:** Đã chấp nhận
- **Ngày:** 2026-11-06 (test chạy 08/11 cho kiểm thuốc, 09/11 cho OCR)
- **Người quyết:** phụ trách AI

## Bối cảnh

Lỗi nguy hiểm nhất là báo xanh khi trên tay có viên sai. Accuracy hay F1 không đo được lỗi này.

## Quyết định

- **Chỉ số chính:** chấp nhận nhầm cấp cảnh khi tráo 1 viên đúng bằng (a) viên lớp 107, (b) viên lớp đã biết ngoài đơn; mỗi cảnh 3 lần mỗi loại.
- **Chuẩn:** cận trên CI 95% (bootstrap 1.000 lần theo nhóm đơn) **≤ 2% cho cả hai loại**. Không bao giờ nới; chỉ cải thiện bằng mô hình tốt hơn.
- **Ngưỡng triển khai** 0,0529, fit trên val với mục tiêu 1,8%, nằm trong `deploy_config.json`.
- **Tập test** khóa suốt quá trình chọn, đăng ký trước cách đo, **chạy đúng một lần**. Đã dùng: kiểm thuốc 2026-11-08 (90,2% báo xanh; 1,09% / 1,31%), OCR 2026-11-09 (99,85% dòng đúng).

## Hệ quả

- Không ai (người hay AI agent) được chạy lại đánh giá trên test, chỉnh ngưỡng, hay sửa `deploy_config.json` theo kết quả test. Code đánh giá vẫn khóa bằng cờ `--unseal-test`.
- Mọi thay đổi mô hình sau này phải đo trên val và cần một tập test mới.
- Số đo dùng viên lạ cùng nguồn dữ liệu, có thể lạc quan với thuốc hoàn toàn mới (đã khai báo).
