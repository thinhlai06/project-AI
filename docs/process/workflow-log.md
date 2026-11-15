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
| 2026-11-15 | ST-00 | S3 | `deployment.md` mục 2b: lệnh `pip install -r backend` + gạch chéo ngược + `requirements.txt` bị vỡ thành 2 dòng (`-r backend` / `equirements.txt`). Quét `docs/**/*.md` thì chỉ có chỗ này. Khi kiểm lại, chính lệnh kiểm của Claude (chuỗi có gạch chéo ngược + r trong lệnh Bash) cũng bị biến dạng y hệt | Chuỗi "gạch chéo ngược + r" bị hiểu thành ký tự xuống dòng/CR ở lớp truyền văn bản giữa model và công cụ (không phải lỗi của Qoder); chưa rõ chính xác lớp nào | Qoder sửa bằng cách đưa nguyên văn; Claude kiểm bằng `chr(92)` ở mức byte (1 token đúng, 0 byte CR, không còn dòng mồ côi) | ai-workflow mục 3 | Đã áp dụng (mục 3, chủ dự án duyệt 2026-11-15): khi viết hoặc kiểm chuỗi có gạch chéo ngược trước r/n/t (đường dẫn Windows), kiểm bằng byte (`chr(92)`), ưu tiên đường dẫn dùng dấu `/` |
| 2026-11-15 | ST-00 | S3 | Qoder `accept_edits` **không chạy được** `.venv\Scripts\python.exe` (`-c`, `py_compile`, `--help` đều bị cổng quyền chặn); Read/Write/Grep thì dùng bình thường | Cổng quyền của Qoder với shell | Claude chạy `py_compile` và chạy script, review diff thật; không nâng quyền | ai-workflow mục 3 (Claude là bên chạy kiểm) | Đã xử lý (Python đã đo; `flutter` còn phải đo ở ST-01) |
| 2026-11-15 | ST-00 | S3 | Cách làm tốt: script dùng một lần (`.ai-work/ST-00/run_d1_d4.py`) do Qoder viết, Claude review lần 1, subagent review độc lập lần 2 (không có lỗi chặn; 5 điểm nhỏ đã sửa qua Qoder: mất bằng chứng khi lỗi giữa chừng, lộ `raw_name` trong thông báo lỗi, D3 chưa kiểm câu `summary`, chỉ kiểm lượt đầu, proxy hệ thống), rồi chạy thật 2 lần và 1 ca âm tính (server không tồn tại thì thoát mã 1) | – | Giữ quy trình "viết → review 2 lần → chạy thử cả ca dương và âm" cho mọi script kiểm | – | Theo dõi |
| 2026-11-15 | ST-00 | S3 | Đo D1–D4 thấy **lần gọi đầu sau khi server rảnh chậm hơn hẳn**: đọc đơn 582 mất 8,34 s (lần sau 4,24 s), kiểm D1 lần đầu 4,23 s (lần sau 0,85–0,90 s) | Làm nóng mô hình / bộ nhớ đệm của ONNX Runtime | Ghi lại; số ST-00 lấy từ lần chạy lúc đã nóng | Chưa có | Đề xuất cho ST-05.2 (`measure_latency.py`): bỏ 1 lần gọi làm nóng khỏi trung bình và báo riêng thời gian lần đầu, vì NFR-02 (kiểm ≤ 3 s, đọc đơn ≤ 10 s) bị lần đầu chạm ngưỡng |
| 2026-11-15 | ST-00 | S3 | Harness của Claude Code gợi ý thêm dòng đồng tác giả AI vào commit/PR, trái AGENTS.md (mục Quy tắc) và ai-workflow mục 6 | Cấu hình công cụ khác luật repo | Tuân luật repo: commit/PR của story không có dòng `Co-Authored-By` hay "Generated with" | ai-workflow mục 6 | Theo dõi (chưa đề xuất đổi luật; chủ dự án chọn chỉ ghi nhật ký) |
| 2026-11-15 | ST-00 | S3 | Hỏi "Qoder đã được yêu cầu mở máy ảo để test chưa": ai-workflow mục 4 chỉ ghi "chạy trên emulator" mà không nói ai làm, không có tên AVD, đường dẫn SDK hay lệnh; mẫu prompt Qoder không nhắc emulator | Luồng viết trước khi đo được Qoder không chạy được shell | Thêm mục 4b: Claude mở emulator (tên AVD, đường dẫn, lệnh, dọn dẹp); lệnh chưa chạy thử, kiểm ở ST-01.3 | ai-workflow mục 4b | Đã áp dụng (mục 4b, chủ dự án duyệt 2026-11-15) |
| 2026-11-15 | ST-00 | S3 | Workflow chỉ có "review PR tối đa 3 vòng": thiếu prompt review chuẩn, tiêu chí "đạt" và cổng merge; bảng vai trò cấm Claude merge | Thiếu đặc tả | Thêm mục 5b (prompt review chuẩn, vòng review, kiểm theo loại PR, cổng merge 7 điều) và cho phép Claude merge khi cổng đạt **và** chủ dự án cho phép bằng lời cho đúng PR đó; sửa mục 1, 2 (bước 8, 9), 7 | ai-workflow mục 5b | Đã áp dụng (mục 5b, chủ dự án duyệt 2026-11-15) |

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
