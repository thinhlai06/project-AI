# Nhật ký vận hành luồng Claude + Qoder

> **Trả lời câu hỏi:** đã gặp trục trặc gì khi làm việc, xử lý ra sao, luật nào đã đổi.
> Cách ghi và quy trình xử lý: [ai-workflow.md](ai-workflow.md) mục 8. Mới nhất ở **dưới cùng**.
> Mức: **S1** suýt mất việc / lộ file cấm / commit sai nhánh · **S2** mất thêm ≥ 1 vòng · **S3** gợi ý, cách làm tốt.

## Ghi chép ở dự án này

| Ngày | Story | Mức | Tình huống | Nguyên nhân | Cách xử lý | Luật liên quan | Trạng thái |
|---|---|---|---|---|---|---|---|
| 2026-11-15 | docs | S2 | `tasks.csv` bị ghi đè bằng bản tab-separated, **mất dấu tiếng Việt** (chữ có dấu thành `?`) | Mở và lưu bằng Excel (lưu dạng ANSI) | Khôi phục từ git; không mất chỉnh sửa vì trạng thái giống bản gốc | Backlog mục 1: không mở/lưu `tasks.csv` bằng Excel; theo dõi bằng Google Sheets (Import) | Đã xử lý |
| 2026-11-15 | docs | S2 | `.gitignore` là danh sách cho phép (`/*`): thư mục mới (`anh_demo/`, `docs/design/`, file `Dockerfile`) bị bỏ qua, `git add` không thấy | Thiết kế của `.gitignore` | Mở khóa từng đường dẫn bằng commit riêng; thêm luật kiểm `git check-ignore -v` trước khi add | ai-workflow 2b.3-9 | Đã áp dụng (2b.3-9) |
| 2026-11-15 | docs | S2 | `backlog.md` và `tasks.csv` được **sinh bằng script**; mỗi lần sinh lại ghi đè các chỉnh sửa tay trong `backlog.md` (ghi chú nhập Sheets mất 3 lần) | Script nằm ở thư mục tạm của phiên, không có trong repo | Sửa script để chứa ghi chú; **từ nay `backlog.md` và `tasks.csv` là nguồn, sửa tay, không sinh lại** (script không còn) | Backlog mục 1 | Đã xử lý |
| 2026-11-15 | docs | S3 | Lệnh bash nhiều dòng với nhiều dấu nháy lỗi cú pháp (`unexpected EOF`) | Dấu nháy lồng trong heredoc | Viết script ra file bằng công cụ Write rồi chạy | – | Theo dõi |
| 2026-11-15 | design | S3 | Công cụ đăng thiết kế chặn đọc file ở thư mục tạm của phiên; thư mục làm việc trong repo (`.design-work/`, loại khỏi git) chạy được | Quyền đọc theo đường dẫn | Dùng `.design-work/` | – | Theo dõi |
| 2026-11-15 | docs | S3 | Kiểm tự động tham chiếu chéo (mã FR/UC/TC/ADR, thứ tự phụ thuộc, màn thiết kế) bắt được khoảng trống mà đọc bằng mắt bỏ sót (FR-PRES-07 chưa có task) | – | Giữ cách kiểm này mỗi khi đổi lớn tài liệu | readiness.md mục 5 | Đã áp dụng |

## Bài học mang sang từ một dự án trước (chưa kiểm chứng ở dự án này)

Nguồn: nhật ký vận hành của một dự án .NET dùng cùng luồng (Claude điều phối, Qoder viết code, worktree). Đây là **giả thuyết cần kiểm ở lần chạy đầu**; khi xảy ra thật hoặc được loại trừ, chuyển lên bảng trên và đổi trạng thái.

| Bài học | Việc kiểm ở dự án này | Trạng thái |
|---|---|---|
| Qoder ở chế độ `accept_edits` **không chạy được công cụ build** (`dotnet`) | Lần đầu giao phase, đo xem Qoder có chạy được `flutter analyze`/`flutter test` không; ghi kết quả | Theo dõi |
| `qodercli -c` nối vào session gần nhất của **bất kỳ** worktree, gây nhầm chéo task | Đã đưa thành luật cấm (ai-workflow mục 3); kiểm lại khi dùng subagent | Đã áp dụng |
| Qoder **không xóa/đổi tên được file**, chỉ làm rỗng | Kiểm khi có task xóa file; Claude `git rm -f` sau khi đọc diff | Theo dõi |
| `git add` một đường dẫn bị ignore **hủy cả lệnh add** | Luật 2b.3-9: đọc `git diff --cached --name-only` trước khi commit | Đã áp dụng |
| Báo cáo của subagent không đáng tin | Luật 2b.7: tự đọc diff và tự chạy kiểm | Đã áp dụng |
| Squash merge làm `rebase` thường sai cho nhánh xếp chồng | Luật 2b.4: dùng `rebase --onto origin/main <cha> <con>` | Đã áp dụng |
| Rebase khi Qoder đang chạy làm hỏng phase dở | Luật 2b.4 | Đã áp dụng |
| Lỗi cú pháp lặp lại của model (nhầm dấu, thiếu `return`) | Theo dõi kiểu lỗi của Dart/Flutter; thêm câu nhắc vào prompt khi lặp | Theo dõi |
| So sánh trước/sau bằng script chạy API trên cổng riêng cho bằng chứng rõ hơn chỉ nhìn test xanh | Dùng `backend/measure_latency.py` (ST-05) và kịch bản D1–D4 làm bằng chứng cho story gọi server | Theo dõi |
