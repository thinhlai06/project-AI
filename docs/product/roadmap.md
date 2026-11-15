# Lộ trình và backlog

> **Trả lời câu hỏi:** làm gì trước, làm gì sau, xong khi nào.
> AI agent làm **theo thứ tự task** trong [backlog.md](backlog.md), mỗi lần một story, xong thì đổi trạng thái trong [tasks.csv](tasks.csv).
> Cập nhật: 2026-11-15 · Hạn cuối: 31/12/2026

## 1. Mốc

| Mốc | Thời gian | Kết quả | Trạng thái |
|---|---|---|---|
| M0 – Nền móng | 14–16/11 | Bộ tài liệu duyệt xong, repo gọn, README mới, Docker, ảnh demo, backlog | 🔄 |
| M1 – Khung app | 17–23/11 | Dự án Flutter, theme, router, database, cài đặt server + kiểm kết nối, client API; **cổng 22/11**: đo tốc độ trên laptop trình bày | ⏳ |
| M2 – Đơn → lịch | 24–30/11 | Nhập đơn, màn xác nhận, sửa dòng, lưu lịch, màn Hôm nay | ⏳ |
| M3 – Nhắc + kiểm cữ | 1–9/12 | Nhắc cục bộ, màn Cữ cần uống, chụp, gửi, màn kết quả, TTS | ⏳ |
| M4 – Hoàn thiện luồng | 10–16/12 | Chụp lại, "Tôi đã uống", tự kiểm vỏ hộp, chống uống lặp, lịch sử, đơn mẫu, lần đầu dùng | ⏳ |
| M5 – Ổn định | 17–22/12 | Kiểm thử theo [test-plan](../quality/test-plan.md), sửa lỗi, tiếp cận; thử cài iPhone nếu mượn được Mac | ⏳ |
| M6 – Trình bày | 23–31/12 | Báo cáo, quay video dự phòng, tập demo trên laptop trình bày | ⏳ |

## 2. Backlog

Danh sách story và task, mô tả chi tiết, ước lượng, phụ thuộc: [backlog.md](backlog.md). Bảng theo dõi trạng thái từng task (Todo/Doing/Review/Done/Blocked): [tasks.csv](tasks.csv). **Trạng thái chỉ ghi ở `tasks.csv`**, không ghi lại ở đây.

Nếu trễ: bỏ từ dưới lên theo ưu tiên (Could → Should); không bỏ Must. Thứ tự gợi ý khi cắt: ST-22 → ST-19 → ST-21 → ST-17.1 → ST-18.1.

Một người làm toàn bộ (Claude lập plan và review, Qoder CLI viết code); thứ tự làm nằm ở cột `Thứ tự làm` của [tasks.csv](tasks.csv).
