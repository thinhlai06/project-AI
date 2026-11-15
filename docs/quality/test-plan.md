# Kế hoạch kiểm thử

> **Trả lời câu hỏi:** kiểm cái gì, bằng cách nào, khi nào thì coi là đạt.
> Yêu cầu: [../product/prd.md](../product/prd.md). Cập nhật: 2026-11-15 · Trạng thái: **đã chốt**

## 1. Các tầng kiểm thử

| Tầng | Phạm vi | Công cụ | Chạy khi | Có sẵn |
|---|---|---|---|---|
| AI hồi quy | Hàm đánh giá, chấm điểm trên embedding cố định | `tests/test_eval.py` (7 bài) | Đổi `medicheck_ai/` | ✅ (chỉ máy phụ trách AI) |
| Server – logic quyết định | Xanh/đỏ/vàng, chỉ nhắc lịch, lớp không đo được | `backend/tests/test_decide.py` | Đổi `backend/` | ✅ |
| Server – hợp đồng | `openapi.yaml` khớp code | `python -m backend.export_openapi` rồi `git diff --exit-code docs/architecture/openapi.yaml` | Đổi `app.py` | ✅ |
| App – unit | `core/domain`: chọn cữ hiện tại, dựng payload, tính ngày kết thúc, đổi `schedule` → `amount_halves`, gộp kết quả chụp lại | `flutter test` | Mỗi commit | ⏳ |
| App – widget | SCR-CONFIRM, SCR-RESULT (đủ 5 trường hợp nút), SCR-DOSE | `flutter test` | Mỗi commit | ⏳ |
| App – tích hợp | Luồng nhập đơn → xác nhận → kiểm cữ với server thật | `integration_test` trên máy giả lập | Trước mỗi mốc | ⏳ |
| Thủ công | Kịch bản demo, tiếp cận, mất mạng | Checklist mục 4–5 | Trước mỗi mốc, trước buổi trình bày | ⏳ |

Không chạy lại đánh giá trên tập test của mô hình ([ADR-008](../architecture/adr/safety-rule-and-sealed-test.md)).

## 2. Ca kiểm thử bắt buộc cho app (gắn với quy tắc nghiệp vụ)

| Mã | Ca | Mong đợi | Quy tắc |
|---|---|---|---|
| TC-01 | Server trả `status = not_green` / `partial` | Không có nút "Tôi đã uống" | BR-01 |
| TC-02 | Timeout, mất mạng, JSON hỏng, HTTP 500 | MSG-NO-SERVER, không xanh, có lối tự kiểm | BR-01, FR-VER-08 |
| TC-03 | Đơn có dòng `missing_schedule` | Dòng bị khóa, "Đúng rồi, tạo lịch" bị khóa tới khi chọn lịch hoặc "Để sau" | BR-05 |
| TC-04 | Dòng `name = null` | `check_mode = reminder_only`, không vào `session_lines`, có trong `unchecked_count` | BR-03 |
| TC-05 | Dòng nửa viên | Nhắc lịch, không chấm ảnh, có trong `unchecked_count` | BR-04 |
| TC-06 | Dòng `as_needed` | Hiện trong đơn, không có nhắc | BR-04 |
| TC-07 | Cữ chỉ có thuốc chỉ nhắc lịch | Không gọi server; MSG-NOT-CHECKABLE | FR-VER-04 |
| TC-08 | Chụp lại lần 2 vẫn chưa xanh | Chỉ còn "Tôi đã kiểm vỏ hộp" | BR-08 |
| TC-09 | Chụp lại: lần 1 xanh 2/3 viên, lần 2 xanh viên còn lại | Cữ xanh, payload lần 2 chỉ có dòng còn thiếu với `count` còn lại | FR-VER-07 |
| TC-10 | Mở cữ đã uống | "Cữ sáng đã uống lúc …", không kiểm lại | FR-LOG-03 |
| TC-11 | Tên thuốc có dấu | Gửi/nhận đúng UTF-8 | NFR-07 |
| TC-12 | Xóa đơn | Hủy mọi nhắc của đơn; file ảnh đơn bị xóa; lịch sử cữ còn | FR-PRES-10 |
| TC-13 | Khởi động lại máy | Nhắc vẫn đến đúng giờ | FR-REM-01 |
| TC-14 | Chế độ máy bay | Lịch, nhắc, ghi nhận, lịch sử chạy được | NFR-03 |
| TC-15 | Không có chuỗi chữ cấm ("an toàn", tên màu viên…) | `grep` trên `strings_vi.dart` sạch | ui-ux-spec mục 5 |
| TC-16 | Có đơn đang dùng, nhập và lưu đơn mới | Hiện MSG-REPLACE-PRES; sau khi lưu chỉ còn 1 đơn `active`; nhắc đơn cũ bị hủy; chèn thẳng đơn `active` thứ hai vào database bị từ chối | BR-12, FR-PRES-11 |
| TC-17 | Bấm "Hủy" ở SCR-CONFIRM khi đã có đơn đang dùng | Đơn cũ giữ nguyên `active`, nhắc không đổi | BR-12 |
| TC-18 | Gửi người thân từ chi tiết đơn | Hiện MSG-SHARE-WARN trước; bảng chia sẻ có ảnh đơn gốc, ảnh phiếu (đủ cột, có chú thích), bản chữ; không có họ tên, số BHYT trong phiếu và bản chữ | FR-PRES-09, ADR-016 |
| TC-19 | Ở màn chụp, bấm "Chọn ảnh có sẵn" và chọn ảnh thuốc trong thư viện (máy giả lập) | Ảnh được chuẩn bị ≤ 2048 px, gửi với `frame = null`, hiện SCR-RESULT; không cần quyền camera | FR-VER-10 |

## 3. Tiêu chí đạt của một mốc

- Mọi ca Must liên quan tới mốc đạt; không còn lỗi làm sai BR-01 hay BR-10.
- `flutter analyze` không lỗi; `flutter test` xanh; test của server xanh.
- Kịch bản demo (mục 5) chạy trọn trên máy giả lập.

## 4. Kiểm tiếp cận và hiệu năng

- Checklist tiếp cận ở [../product/ui-ux-spec.md](../product/ui-ux-spec.md) mục 7 cho từng màn.
- Bật cỡ chữ hệ thống lớn nhất và TalkBack, đi trọn luồng kiểm một cữ.
- Đo trên laptop trình bày (cổng 22/11): đọc đơn ≤ 10 giây, kiểm cữ 4 viên ≤ 3 giây (NFR-02). Ghi kết quả vào [../architecture/deployment.md](../architecture/deployment.md).

## 5. Kịch bản demo (dữ liệu tập test VAIPE, mô hình chưa từng học)

| Cảnh | Đơn | Cữ | Ảnh thuốc | Mong đợi |
|---|---|---|---|---|
| D1 – Xanh | `don_thuoc_582.png` | Sáng | `anh_thuoc_A1_582_2.jpg` | Xanh: "Đúng hết. 3 viên khớp cữ sáng." |
| D2 – Xanh | `don_thuoc_979.png` | Chiều | `anh_thuoc_A2_979_3.jpg` | Xanh: 4 viên khớp cữ chiều |
| D3 – Thiếu viên | `don_thuoc_979.png` | Sáng | `anh_thuoc_A2_979_3.jpg` | Không xanh: "Còn thiếu 1 viên kavasdin 5 5mg." |
| D4 – Thừa viên | `don_thuoc_582.png` | Sáng | `anh_thuoc_A2_979_3.jpg` | Không xanh: "Có 1 viên app chưa xác nhận được." |
| D5 – Tay thật | bất kỳ | bất kỳ | chụp bằng webcam | Câu kết quả hợp lý; chủ yếu để minh họa thao tác |

Các ảnh trên nằm ở [../../anh_demo/](../../anh_demo/) (đã chạy thử 15/11 trên server Docker: D1 xanh 3/3, D2 xanh 4/4, D3 thiếu kavasdin, D4 thừa 1 viên; ~1 giây mỗi lần kiểm). App chép chúng vào `mobile/assets/demo/` ở ST-16.1.
