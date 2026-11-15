# Lộ trình và backlog

> **Trả lời câu hỏi:** làm gì trước, làm gì sau, xong khi nào.
> AI agent làm **theo thứ tự story**, mỗi lần một story, xong thì đánh dấu ✅ ở đây.
> Cập nhật: 2026-11-15 · Hạn cuối: 31/12/2026

## 1. Mốc

| Mốc | Thời gian | Kết quả | Trạng thái |
|---|---|---|---|
| M0 – Nền móng | 14–16/11 | Bộ tài liệu duyệt xong, repo gọn, README mới | 🔄 |
| M1 – Khung app | 17–23/11 | Dự án Flutter, theme, router, database, cài đặt server + kiểm kết nối, client API; **cổng 22/11**: đo tốc độ trên laptop trình bày | ⏳ |
| M2 – Đơn → lịch | 24–30/11 | Nhập đơn, màn xác nhận, sửa dòng, lưu lịch, màn Hôm nay | ⏳ |
| M3 – Nhắc + kiểm cữ | 1–9/12 | Nhắc cục bộ, màn Cữ cần uống, chụp, gửi, màn kết quả, TTS | ⏳ |
| M4 – Hoàn thiện luồng | 10–16/12 | Chụp lại, "Tôi đã uống", tự kiểm vỏ hộp, chống uống lặp, lịch sử, đơn mẫu, lần đầu dùng | ⏳ |
| M5 – Ổn định | 17–22/12 | Kiểm thử theo [test-plan](../quality/test-plan.md), sửa lỗi, tiếp cận; thử cài iPhone nếu mượn được Mac | ⏳ |
| M6 – Trình bày | 23–31/12 | Báo cáo, quay video dự phòng, tập demo trên laptop trình bày | ⏳ |

## 2. Backlog (theo thứ tự làm)

| Mã | Story | Yêu cầu | Mốc | Trạng thái |
|---|---|---|---|---|
| ST-00 | Chép ảnh demo và crop ảnh mẫu từ thư mục chờ xóa vào repo (trước khi xóa) | FR-DEMO-01, FR-DOSE-02 | M0 | ⏳ |
| ST-01 | Tạo dự án Flutter `mobile/`, khóa phiên bản, `flutter analyze` sạch, cấu hình cleartext Android + quyền iOS | NFR-08 | M1 | ⏳ |
| ST-02 | Theme theo design tokens, `strings_vi.dart`, khung điều hướng `go_router` | NFR-04 | M1 | ⏳ |
| ST-03 | Database `drift` theo [erd.md](../architecture/erd.md), bật foreign keys, test DAO | – | M1 | ⏳ |
| ST-04 | Client API + DTO theo `openapi.yaml`, timeout, xử lý lỗi; màn Cài đặt server + "Kiểm tra kết nối" | FR-SET-01 | M1 | ⏳ |
| ST-05 | Đo tốc độ trên laptop trình bày (cổng 22/11) | NFR-02 | M1 | ⏳ |
| ST-06 | Nhập đơn từ file + màn chờ + lỗi | FR-PRES-01, 03 | M2 | ⏳ |
| ST-07 | Màn xác nhận + sửa dòng (catalog) + lưu đơn (thay đơn cũ, lưu ảnh đơn) | FR-PRES-04 … 06, 11, FR-SCH-01 | M2 | ⏳ |
| ST-08 | `core/domain`: dòng còn hiệu lực, ngày kết thúc, cữ hiện tại (unit test) | FR-SCH-02, 03, FR-DOSE-03 | M2 | ⏳ |
| ST-09 | Màn Hôm nay + danh sách/chi tiết đơn + kết thúc/xóa đơn | FR-PRES-08, 10, 12 | M2 | ⏳ |
| ST-10 | Nhắc cục bộ + nhắc lại + mở đúng cữ từ thông báo | FR-REM-01 … 03 | M3 | ⏳ |
| ST-11 | Màn Cữ cần uống + TTS | FR-DOSE-01, NFR-05 | M3 | ⏳ |
| ST-12 | Màn chụp (khung, camera, chọn ảnh có sẵn, chuẩn bị ảnh 2048 px) | FR-VER-01, 02, 10 | M3 | ⏳ |
| ST-13 | Dựng payload + gọi verify + màn kết quả (khoanh viên, nút theo trạng thái) | FR-VER-03 … 06, 08, 09 | M3 | ⏳ |
| ST-14 | Chụp lại 1 lần + gộp kết quả | FR-VER-07 | M4 | ⏳ |
| ST-15 | "Tôi đã uống", tự kiểm vỏ hộp, chống uống lặp | FR-LOG-01 … 03 | M4 | ⏳ |
| ST-16 | Đơn mẫu + ảnh thuốc mẫu | FR-ONB-01, FR-DEMO-01 | M4 | ⏳ |
| ST-17 | Lần đầu dùng (hướng dẫn giọng nói), cảnh báo không thay dược sĩ | FR-ONB-02, FR-SET-03 | M4 | ⏳ |
| ST-18 | Lịch sử 7 ngày, đổi giờ nhắc, bật/tắt giọng nói | FR-LOG-04, FR-REM-04, FR-SET-02 | M4 | ⏳ |
| ST-19 | Chụp đơn giấy | FR-PRES-02 | M4 | ⏳ |
| ST-20 | Ảnh mẫu thuốc trên màn Cữ cần uống | FR-DOSE-02 | M5 | ⏳ |
| ST-21 | Gửi người thân: ảnh đơn gốc + ảnh phiếu bảng + chữ (SCR-SHARE) | FR-PRES-09 | M5 | ⏳ |
| ST-22 | Thử cài lên iPhone | ADR-002 | M5 | ⏳ |

Nếu trễ: bỏ từ dưới lên (ST-22 → ST-19); không bỏ story Must.

## 3. Phân công gợi ý

| Người | Phần chính |
|---|---|
| Phụ trách AI | Server, hợp đồng API, ST-00, ST-04, ST-05, ST-08, ST-13; review mọi chỗ chạm BR-01 |
| Mobile 1 | ST-01 … ST-03, ST-06, ST-07, ST-09, ST-16, ST-19 |
| Mobile 2 | ST-10 … ST-12, ST-14, ST-15, ST-17, ST-18, ST-20, ST-21 |
