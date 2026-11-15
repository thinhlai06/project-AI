# Tài liệu yêu cầu sản phẩm (PRD)

> **Trả lời câu hỏi:** app phải làm gì, đến mức nào thì coi là xong.
> **Nguồn trên nó:** [business-analysis.md](business-analysis.md) (mục tiêu, quy tắc BR-xx). **Nguồn dưới nó:** [use-cases.md](use-cases.md), [ui-ux-spec.md](ui-ux-spec.md), [../architecture/openapi.yaml](../architecture/openapi.yaml).
> Cập nhật: 2026-11-15 · Phiên bản: MVP 1.0 · Trạng thái: **đã chốt**

Mức ưu tiên: **Must** = thiếu thì không demo được · **Should** = nên có trong MVP · **Could** = làm nếu còn thời gian · **Won't** = giai đoạn 2.

## 1. Tóm tắt sản phẩm

MediCheck là app Flutter, ưu tiên Android, kèm một server AI chạy trên laptop. App lưu mọi dữ liệu trên máy, không có tài khoản. Server không lưu gì: chỉ nhận ảnh, chạy mô hình và trả kết quả. Người dùng chính là người cao tuổi tự dùng, mắt kém.

## 2. Yêu cầu chức năng

### 2.1. Nhập và xác nhận đơn (PRES)

| Mã | Yêu cầu | Ưu tiên | Tiêu chí chấp nhận |
|---|---|---|---|
| FR-PRES-01 | Chọn ảnh (PNG/JPEG) hoặc PDF đơn từ máy, gửi `POST /v1/prescriptions/parse` | Must | Đơn mẫu 582 và 979 ra đúng các dòng thuốc như trong [test-plan.md](../quality/test-plan.md) |
| FR-PRES-02 | Chụp đơn giấy bằng camera (đường phụ), có lời hướng dẫn lần đầu | Should | Ảnh chụp được gửi giống FR-PRES-01 |
| FR-PRES-03 | Màn chờ khi đọc đơn: câu nói "Đang đọc đơn, xin chờ khoảng 10 giây", không cho bấm lại | Must | Thời gian chờ tối đa 30 giây, quá hạn thì báo lỗi kèm nút thử lại |
| FR-PRES-04 | Màn xác nhận **bắt buộc** với mọi đơn: mỗi dòng là một thẻ chữ to (tên, số viên mỗi buổi, trước/sau ăn) | Must | Không có đường nào tạo lịch mà bỏ qua màn này (BR-02) |
| FR-PRES-05 | Dòng có `needs_review = true` hoặc `dose_type = missing_schedule` được tô nổi; các dòng khác chỉ cần một nút "Đúng rồi" chung | Must | Dòng thiếu lịch hiện "Chưa có lịch" và bị khóa cho đến khi chọn lịch (BR-05) |
| FR-PRES-06 | Sửa một dòng bằng cách **chọn**: tên thuốc chọn từ danh sách `GET /v1/catalog` (có tìm kiếm), buổi và số viên chọn bằng nút lớn | Must | Không có ô gõ tự do cho số viên; tên ngoài danh mục được giữ nhưng chỉ nhắc lịch (BR-03) |
| FR-PRES-07 | Đọc to toàn bộ lịch đã đọc trên màn xác nhận (nút 🔊) | Should | Câu đọc theo mẫu ở [ui-ux-spec.md](ui-ux-spec.md) |
| FR-PRES-08 | Hiện "Bệnh: …" (chẩn đoán) trong chi tiết đơn; chỉ hiển thị (BR-09) | Should | Chẩn đoán không gửi lại server, không dùng cho kiểm thuốc |
| FR-PRES-09 | Gửi người thân kiểm tra qua bảng chia sẻ của hệ điều hành (Zalo, tin nhắn), từ SCR-CONFIRM và SCR-PRES-DETAIL. Gửi 3 thứ: (1) **ảnh đơn gốc**; (2) **ảnh "Phiếu đơn app đọc được"** do app vẽ: bảng chữ to, cột STT · Tên thuốc · SL · Sáng · Trưa · Chiều · Tối · Ghi chú, dòng chỉ nhắc lịch / thiếu lịch có chú thích; (3) bản chữ cùng nội dung trong tin nhắn | Could | Bố cục phiếu theo [ui-ux-spec.md](ui-ux-spec.md) SCR-SHARE; người dùng luôn thấy câu "Ảnh đơn có họ tên và số BHYT của bác" trước khi gửi (ADR-016) |
| FR-PRES-10 | Xóa một đơn: xóa đơn, các dòng thuốc, lịch, nhắc và ảnh đơn đã lưu | Must | Sau khi xóa, không còn thông báo nào của đơn đó và file ảnh đơn đã bị xóa |
| FR-PRES-11 | Mỗi lúc chỉ có **một đơn đang dùng** (BR-12). Lưu đơn mới khi đã có đơn đang dùng: SCR-CONFIRM báo trước "Đơn cũ (kê ngày …) sẽ kết thúc"; khi lưu, đơn cũ chuyển `ended`, hủy nhắc của đơn cũ; lịch sử cữ giữ nguyên | Must | Không có thời điểm nào có 2 đơn `active` (ràng buộc database) |
| FR-PRES-12 | "Kết thúc đơn" trong chi tiết đơn (xác nhận 2 bước): đơn chuyển `ended`, hủy nhắc, vẫn xem lại được | Should | |

### 2.2. Lịch và nhắc thuốc (SCH, REM)

| Mã | Yêu cầu | Ưu tiên | Tiêu chí chấp nhận |
|---|---|---|---|
| FR-SCH-01 | Tạo lịch uống theo 4 buổi từ các dòng đã xác nhận; ngày bắt đầu = ngày xác nhận | Must | Mỗi dòng `regular`/`half_pill` có ≥ 1 buổi; `as_needed` không có lịch nhắc |
| FR-SCH-02 | Ngày kết thúc của mỗi dòng = ngày bắt đầu + ⌈số lượng ÷ số viên mỗi ngày⌉ − 1; dòng không có số lượng thì không có ngày kết thúc | Should | Hết ngày kết thúc thì dòng không còn trong cữ; mọi dòng đã hết thì đơn tự chuyển `ended` (OQ-02) |
| FR-SCH-03 | Cữ chỉ gồm các dòng còn hiệu lực của **đơn đang dùng**; không gộp nhiều đơn | Must | Xem OQ-01, BR-12 |
| FR-REM-01 | Nhắc cục bộ theo giờ mặc định Sáng 7:00, Trưa 11:30, Chiều 17:00, Tối 20:00; chỉ nhắc buổi có thuốc | Must | Nhắc vẫn chạy khi tắt mạng và sau khi khởi động lại máy |
| FR-REM-02 | Nội dung nhắc: "Đến giờ uống thuốc sáng, 3 viên." | Must | Số viên = tổng số viên của cữ (kể cả nửa viên tính là 1 viên) |
| FR-REM-03 | Chưa bấm "Tôi đã uống" thì nhắc lại sau 15 phút, tối đa 2 lần | Should | Bấm "Tôi đã uống" thì hủy các lần nhắc lại |
| FR-REM-04 | Đổi giờ từng buổi trong cài đặt; không hỏi lúc cài app | Should | Đổi giờ thì lên lịch lại mọi nhắc |

### 2.3. Kiểm thuốc theo cữ (DOSE, VER)

| Mã | Yêu cầu | Ưu tiên | Tiêu chí chấp nhận |
|---|---|---|---|
| FR-DOSE-01 | Màn "Cữ sáng cần uống": tên chữ to, số viên từng thuốc, trước/sau ăn, nút đọc to | Must | Mở được từ thông báo và từ màn Hôm nay |
| FR-DOSE-02 | (bỏ) Ảnh mẫu từng thuốc. Thay bằng FR-VER-11 | – | Quyết định 2026-11-15, [ADR-018](../architecture/adr/pill-crops-in-memory.md) |
| FR-DOSE-03 | Cữ hiện tại = cữ chưa uống gần nhất đã đến giờ trong ngày; người dùng đổi được cữ bằng nút lớn | Must | 9:30 sáng chưa uống cữ sáng → mở ra là cữ sáng |
| FR-VER-01 | Màn chụp: xem trước camera với **khung ngắm** chữ nhật đứng (bốn góc chữ L, dấu + ở giữa, vùng ngoài tối), một nút chụp to, hai nút phụ "Ảnh có sẵn" (FR-VER-10) và "Hướng dẫn" (mở lại hướng dẫn lần đầu), câu hướng dẫn "Xòe bàn tay ra, đặt thuốc lên lòng bàn tay, các viên rời nhau, rồi chụp" | Must | Gửi `frame` khớp với khung ngắm trên màn hình |
| FR-VER-02 | Trước khi gửi: xoay theo EXIF, thu cạnh dài 2048 px, JPEG q85 | Must | Ảnh gửi đi ≤ 2048 px, ~300 KB |
| FR-VER-03 | Dựng `payload` từ database: `session_lines` (dòng chấm ảnh của cữ), `other_lines` (mọi dòng còn hiệu lực khác của đơn đang dùng, kèm buổi), `unchecked_count` (viên chỉ nhắc lịch và nửa viên của cữ) | Must | Đúng quy tắc ở [../architecture/system-architecture.md](../architecture/system-architecture.md) mục 5 |
| FR-VER-04 | Cữ không có dòng chấm ảnh nào: không gọi server, hiện "Thuốc của cữ này app chưa kiểm được bằng hình, hãy kiểm theo vỏ hộp" và nút "Tôi đã kiểm vỏ hộp" | Must | Không gửi `session_lines` rỗng (server trả 422) |
| FR-VER-05 | Hiện kết quả: đọc `summary` trước, khoanh từng viên theo `box` với màu + biểu tượng + kiểu nét, chạm vào viên thì đọc `message` | Must | Xanh: ✓ nét liền; vàng: ? nét đứt; đỏ: ✗ nét dày |
| FR-VER-06 | `status = green` → nút to "Tôi đã uống". `partial` → "Tôi đã kiểm vỏ hộp" cho phần chưa chấm được. `not_green` → "Chụp lại" (nếu còn lượt) và "Tôi đã kiểm vỏ hộp" | Must | Không có nút "Tôi đã uống" khi chưa xanh mà chưa qua bước kiểm vỏ hộp (BR-01) |
| FR-VER-07 | Chụp lại 1 lần: giữ các viên đã xanh, hướng dẫn bỏ viên đỏ ra, chỉ gửi các dòng còn thiếu với số viên còn lại | Must | Lần thứ hai vẫn chưa xanh thì chỉ còn "Tôi đã kiểm vỏ hộp" (BR-08) |
| FR-VER-08 | Lỗi mạng/timeout/server lỗi: báo "Chưa kết nối được máy kiểm thuốc", cho thử lại và cho "Tôi đã kiểm vỏ hộp" | Must | Không bao giờ hiện xanh khi lỗi |
| FR-VER-09 | Thời gian chờ kiểm thuốc 20 giây, có màn chờ đọc "Đang kiểm thuốc" | Must | |
| FR-VER-10 | Ngoài camera, màn chụp có nút phụ "Chọn ảnh có sẵn" mở bộ chọn ảnh của hệ điều hành (thư viện ảnh); ảnh chọn đi qua cùng bước chuẩn bị FR-VER-02 và gửi với `frame = null` | Should | Chạy được trên máy giả lập không cần camera; kết quả hiện như ảnh chụp (cùng SCR-RESULT) |
| FR-VER-11 | Thuốc theo kết quả: dưới ảnh khoanh, mỗi thuốc một hàng gồm **một ảnh viên** cắt từ ảnh vừa chụp theo `box`, tên, số viên, trạng thái bằng chữ + biểu tượng + kiểu viền. Thuốc còn thiếu là hàng không ảnh ("Còn thiếu n viên"); viên không thuộc thuốc nào ở hàng "Viên chưa xác nhận". Chạm hàng thì viên trên ảnh được nhấn mạnh. Không có ô sửa tên/số viên. Ảnh cắt chỉ ở bộ nhớ (ADR-018) | Should | Không ghi file hay database (TC-20); không tạo ra trạng thái xanh nào ngoài server (BR-01) |

### 2.4. Ghi nhận và lịch sử (LOG)

| Mã | Yêu cầu | Ưu tiên | Tiêu chí chấp nhận |
|---|---|---|---|
| FR-LOG-01 | "Tôi đã uống" (1 chạm) ghi giờ uống, kiểu xác nhận `app_verified`, tắt nhắc của cữ | Must | |
| FR-LOG-02 | "Tôi đã kiểm vỏ hộp" ghi kiểu xác nhận `self_confirmed` | Must | Lịch sử phân biệt được hai kiểu |
| FR-LOG-03 | Mở lại cữ đã uống → "Cữ sáng đã uống lúc 7:05", không cho kiểm lại như cữ mới | Must | Chống uống lặp (P3) |
| FR-LOG-04 | Lịch sử 7 ngày gần nhất: mỗi cữ đã uống / bỏ qua / chưa uống, kiểu xác nhận | Should | |

### 2.5. Lần đầu dùng, demo, cài đặt (ONB, DEMO, SET)

| Mã | Yêu cầu | Ưu tiên | Tiêu chí chấp nhận |
|---|---|---|---|
| FR-ONB-01 | Mở lần đầu: nút to "Chọn đơn thuốc" và nút phụ "Thử với đơn mẫu"; không đăng ký, không đăng nhập | Must | |
| FR-ONB-02 | Lần đầu chụp đơn và lần đầu chụp thuốc: hướng dẫn bằng giọng nói + hình minh họa + "Tôi hiểu rồi"/"Bỏ qua"; nút "Hướng dẫn" ở màn chụp mở lại | Should | Từ lần thứ hai vào thẳng màn chụp |
| FR-DEMO-01 | "Thử với đơn mẫu": nạp đơn mẫu (ảnh VAIPE trong app) và cho chọn ảnh thuốc mẫu thay vì chụp | Must | Chạy được trọn kịch bản demo trên máy giả lập không cần camera |
| FR-SET-01 | Cài đặt địa chỉ server + nút "Kiểm tra kết nối" gọi `GET /health` | Must | Mặc định `http://10.0.2.2:8000` trên máy giả lập |
| FR-SET-02 | Bật/tắt giọng nói (mặc định bật), chỉnh giờ từng buổi | Should | |
| FR-SET-03 | Cảnh báo cố định trong cài đặt và lần đầu dùng: "App hỗ trợ đối chiếu với đơn, không thay thế dược sĩ" | Must | |

## 3. Yêu cầu phi chức năng

| Mã | Nhóm | Yêu cầu | Đo bằng |
|---|---|---|---|
| NFR-01 | An toàn | Cận trên 95% báo xanh nhầm ≤ 2% (đã đạt ở server). App không được thêm đường nào tạo ra xanh | Rà code + test BR-01 |
| NFR-02 | Hiệu năng | Kiểm thuốc ≤ 3 giây từ lúc gửi đến khi đọc kết quả (cữ 4 viên, laptop demo, cùng mạng); đọc đơn ≤ 10 giây | Đo trên laptop demo (cổng 22/11) |
| NFR-03 | Hoạt động khi mất mạng | Lịch, nhắc, "Tôi đã uống", lịch sử chạy không cần mạng; chỉ đọc đơn và kiểm thuốc cần server | Test bật chế độ máy bay |
| NFR-04 | Tiếp cận | Chữ thân ≥ 20 sp, nút chính cao ≥ 56 dp, vùng chạm ≥ 48 dp, tương phản ≥ 4,5 : 1 (mục tiêu 7 : 1 cho chữ chính), không dựa chỉ vào màu | Checklist ở [ui-ux-spec.md](ui-ux-spec.md) mục 7 |
| NFR-05 | Giọng nói | Mọi kết quả quan trọng đọc bằng TTS tiếng Việt; có nút nghe lại trên mỗi màn | Test trên máy giả lập có giọng vi-VN |
| NFR-06 | Riêng tư | Không lưu ảnh thuốc; không lưu họ tên, số BHYT dạng chữ; ảnh đơn gốc chỉ nằm trong bộ nhớ riêng của app và xóa cùng đơn (ADR-016); ảnh cắt viên chỉ ở RAM (ADR-018); ảnh chỉ gửi tới server do người dùng cấu hình hoặc khi người dùng tự bấm gửi; server không ghi ảnh ra đĩa | Rà code |
| NFR-07 | Ngôn ngữ | Giao diện tiếng Việt có dấu; mọi chuỗi gửi/nhận là UTF-8 | Test tên thuốc có dấu |
| NFR-08 | Nền tảng | Android 10 (API 29) trở lên, chạy tốt trên máy giả lập API 34; code không dùng thư viện chỉ có trên Android để còn build được iOS | Build Android; xem [ADR-002](../architecture/adr/flutter-android-first.md) |
| NFR-09 | Bảo trì | Hợp đồng API theo `openapi.yaml`; lỗi phân tích JSON không làm sập app | Test hợp đồng |

## 4. Ngoài phạm vi MVP (Won't)

Tài khoản, đồng bộ đám mây, chế độ người thân theo dõi, làm quen thuốc mới, tương tác thuốc, kiểm hàm lượng, chạy mô hình trên máy, tự động chụp, nhiều người dùng trên một máy, đơn ngoài 2 mẫu VAIPE, đa ngôn ngữ.

## 5. Câu hỏi mở (cần người phụ trách duyệt)

AI agent **không được** tự chọn mục nào chưa "Đã chốt". Câu hỏi mới phát sinh thì thêm dòng `OQ-xx` ở đây với trạng thái "Chờ duyệt" và hỏi người phụ trách.

| Mã | Câu hỏi | Quyết định | Trạng thái |
|---|---|---|---|
| OQ-01 | Cho phép nhiều đơn cùng hiệu lực không? | **Không.** Một đơn đang dùng; đơn mới thay đơn cũ (FR-PRES-11, BR-12) | Đã chốt 2026-11-15 |
| OQ-02 | Khi nào ngừng nhắc một dòng thuốc? | Theo FR-SCH-02 (tính từ số lượng); người dùng tự kết thúc đơn được (FR-PRES-12) | Đã chốt 2026-11-15 |
| OQ-03 | "Gửi người thân" gửi gì? | Ảnh đơn gốc + ảnh phiếu bảng chữ to app vẽ + bản chữ (FR-PRES-09); ảnh đơn lưu trong app để gửi lại được ([ADR-016](../architecture/adr/prescription-image-on-device.md)) | Đã chốt 2026-11-15 |
| OQ-04 | Ảnh minh họa từng thuốc lấy từ đâu? | **Không dùng ảnh VAIPE.** Ảnh viên cắt từ ảnh vừa chụp, chỉ trong bộ nhớ, không lưu (FR-VER-11, ADR-018) | Đã chốt 2026-11-15 |
| OQ-05 | Câu hiển thị lấy từ server hay app tự soạn? | Dùng nguyên `summary`/`message` của server để chỉ có một nguồn câu chữ | Đã chốt 2026-11-15 |
| OQ-06 | Kiểm ảnh mờ/tối trên điện thoại trước khi gửi? | Không ở MVP; chỉ dùng `quality` server trả | Đã chốt 2026-11-15 |
