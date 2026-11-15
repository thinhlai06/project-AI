# Kiểm tra sẵn sàng code

> **Trả lời câu hỏi:** tài liệu, môi trường và quyết định đã đủ để bắt đầu code app chưa.
> Kiểm tra ngày 2026-11-15. Chạy lại khi tài liệu đổi lớn (xem mục 5).

## Kết luận

**Sẵn sàng code.** Tài liệu nhất quán, mọi quyết định đã chốt, thư viện cài được. **Hai việc của chủ dự án** (mục 3) đã xong ngày 2026-11-15; ST-01.1 và ST-01.2 đã làm.

## 1. Tài liệu (kiểm tự động)

Script đọc PRD, BA, use case, UI spec, test plan, backlog, `tasks.csv` rồi đối chiếu mã định danh.

| Kiểm | Kết quả |
|---|---|
| Mã FR/NFR/BR/UC/TC/ADR/OQ được nhắc mà chưa định nghĩa | Không có |
| Yêu cầu FR chưa có task nào trỏ tới | Không có |
| Câu hỏi mở (OQ) chưa chốt | Không có (OQ-01 … OQ-06 đã chốt) |
| ADR còn "Đề xuất" | Không có (ADR-001 … ADR-019 đã chấp nhận hoặc bị thay thế) |
| Tài liệu còn "nháp chờ duyệt" | Không có |
| Task: phụ thuộc trỏ tới task không tồn tại; thứ tự làm sai phụ thuộc | Không có (82 task) |
| Màn thiết kế: HTML và PNG đủ; backlog không trỏ tới màn không có | Đạt (31 màn) |
| Còn nhắc ảnh mẫu VAIPE, ST-20, ST-00.3 ở tài liệu đang dùng | Không có |
| Liên kết tương đối trong mọi file `.md` | Không hỏng |

## 2. Môi trường

| Mục | Trạng thái |
|---|---|
| Flutter 3.50.0 (stable, Dart 3.14.0) ở `D:\flutter`, trỏ tới Android SDK và JDK sẵn có | ✅ |
| Thư viện ở ADR-015 (Riverpod, go_router, drift, http, image, camera, file_picker, thông báo, TTS, share_plus, path_provider; dev: drift_dev, build_runner) | ✅ Cài được cùng nhau trên Flutter 3.50.0; `flutter analyze` sạch trên dự án thử (đã xóa) |
| Máy giả lập Android (`pixel_7_-_api_36_0`, `Medium_Phone_API_37.0`) | ✅ Có sẵn |
| Server AI bằng Docker: `docker compose up --build` | ✅ Chạy tốt trên PC này; D1–D4 đúng kỳ vọng |
| Qoder CLI | ✅ Có trong PATH |
| Kho mã: nhánh `main` đã push, không có thay đổi dở | ✅ |
| Chấp nhận giấy phép Android SDK (`flutter doctor --android-licenses`) | ✅ đã xong: `flutter doctor` báo All Android licenses accepted (kiểm 2026-11-15) |
| Flutter và `PUB_CACHE` trong PATH người dùng | ✅ đã xong: `D:/flutter/bin` có trong PATH người dùng và `PUB_CACHE=D:/flutter_pub_cache` đã đặt (kiểm 2026-11-15) |
| Visual Studio thiếu thành phần C++ | Bỏ qua: app không build cho Windows |

## 3. Việc cần chủ dự án làm trước ST-01

Cả hai việc dưới đây đã xong (2026-11-15).

1. Chạy `D:\flutter\bin\flutter doctor --android-licenses`, gõ `y` cho từng mục (không có giấy phép này thì không build được Android).
2. Thêm `D:\flutter\bin` vào PATH và đặt `PUB_CACHE=D:\flutter_pub_cache` (lệnh ở `docs/process/ai-workflow.md` hoặc hỏi lại); mở terminal mới.

## 4. Rủi ro còn lại (không chặn việc code)

| Rủi ro | Cách xử lý |
|---|---|
| Docker chưa thử trên laptop trình bày | ST-05.1, hạn 22/11; có cách venv dự phòng |
| Phản hồi `partial` chưa có mẫu thật (server trả `not_green` khi có `unchecked_count`) | Thử với server thật khi làm ST-13; màn `partial` dựng theo bảng nút |
| Giấy phép PP-OCRv5 và VietOCR chưa kiểm | ST-27.1 (M5) |
| Tên nhóm trên báo cáo (GROUP 05 hay GROUP_01) | ST-27.2, chờ chủ dự án |
| Khối lượng lớn so với 6 tuần, một người làm | Cắt Could rồi Should theo thứ tự ở `roadmap.md`; làm tuần tự theo cột `Thứ tự làm` |
| Gói thư viện cập nhật có thể đổi API giữa chừng | `pubspec.lock` được commit ở ST-01.1; không nâng cấp khi chưa có lý do |

## 5. Cách chạy lại kiểm tra

Kiểm tra tham chiếu chéo gồm: mọi mã `FR-`, `NFR-`, `BR-`, `UC-`, `TC-`, `ADR-`, `OQ-` được nhắc phải có dòng định nghĩa; mọi FR chưa bị bỏ phải có task trỏ tới; mọi `OQ` phải "Đã chốt"; mọi task có phụ thuộc xếp trước; mọi màn backlog trỏ tới phải có file trong `docs/design/screens/`. Khi đổi lớn tài liệu, nhờ trợ lý chạy lại các kiểm tra này và cập nhật file.

## 6. Bắt đầu

Ở phiên mới: "làm ST-01" (task `Todo` có `Thứ tự làm` nhỏ nhất). Quy trình: [../process/ai-workflow.md](../process/ai-workflow.md).
