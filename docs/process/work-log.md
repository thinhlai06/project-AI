# Báo cáo công việc (mới nhất ở trên)

Mỗi phần việc có một báo cáo ngắn khoảng 100 từ. Phân tích chi tiết từng quyết định nằm ở [../archive/MediCheck_decisions.md](../archive/MediCheck_decisions.md).

---

## Task 10 – Docker cho server (15/11/2026) ✅

**Đã làm:** thêm `Dockerfile`, `.dockerignore`, `docker-compose.yml`; viết ADR-017 (thay điểm "không Docker" của ADR-004); viết lại mục chạy server trong `deployment.md`. Thêm yêu cầu FR-VER-10 "Chọn ảnh có sẵn" ở màn chụp thuốc.

**Kiểm chứng:** build image 1,5 GB; container `healthy`; `/health`, `/v1/catalog`, `/v1/pills/verify`, `/v1/prescriptions/parse` chạy đúng (ảnh trắng: không thấy viên, không có dòng thuốc, đúng kỳ vọng). Chưa thử với ảnh đơn thật vì ảnh demo nằm trong thư mục chờ xóa (đang ở Thùng rác).

**Rủi ro:** Docker Desktop và máy giả lập cùng chiếm RAM; cần thử trên chính laptop trình bày.

---

## Task 9 – Bộ tài liệu cho app và dọn thư mục gốc (15/11/2026) ✅

**Đã làm:** viết bộ tài liệu trong `docs/` để nhóm và AI agent làm app không lệch hướng:
- sản phẩm: BA, PRD, use case, UI/UX, roadmap;
- kiến trúc: system architecture, ERD, deployment, `openapi.yaml` sinh từ code, 16 ADR;
- AI, kiểm thử, quy trình Claude + Qoder;
- `AGENTS.md` ở gốc.

Các file `.md` cũ chuyển vào `docs/archive/`; README viết lại.

**Quyết định đã chốt với chủ dự án:**
- một đơn đang dùng (BR-12);
- gửi người thân kèm ảnh đơn gốc và phiếu bảng chữ to (ADR-016 thay ADR-012);
- demo trên máy giả lập Android;
- mỗi story một nhánh và một PR.

**Phản biện:** schema `payload` thiếu trong OpenAPI nên phải tự thêm. Sổ quyết định mục 8 lỗi thời. Ảnh demo còn nằm trong thư mục chờ xóa (ST-00).

---

## Task 8 – Dọn dự án (14/11/2026) ✅

**Việc đã làm:** gỡ web demo (route `/`, thư mục `static/`), chuyển 129 mục không cần vào `D:\project AI_cho_xoa` (chưa xoá hẳn, bản đồ nằm ở `MANIFEST.txt`): dữ liệu thô VAIPE và dataset bổ sung, bộ nhớ đệm, script thử nghiệm, nhánh train S1, file zip và thư mục demo, báo cáo v5, môi trường `.ocrenv`.

**Giữ lại:** tài liệu, báo cáo v6, `backend/`, mô hình ONNX và PyTorch cuối, chuỗi script tạo dữ liệu và xuất mô hình, 3 kernel train cuối, nhãn v2/v3, file chia fold và kết quả đo chính thức.

**Kiểm tra:** máy chủ vẫn chạy đúng (đọc đơn 582, kiểm ảnh A1 báo xanh), 7/7 kiểm thử `test_eval` và các kiểm thử `backend` đạt. Chưa commit.

---

## Task 7 – Đồng bộ báo cáo Word (10/11/2026) ✅

**Việc đã làm:** tạo bản v6 từ v5 (giữ nguyên v5), bản v6 chỉ dùng số của mô hình cuối. Thêm DINOv3, phần lý thuyết OCR, kết quả test và hai ma trận nhầm lẫn; gộp 3.1 với 3.2 cũ; bỏ phần thử nghiệm sơ bộ. Bảng, chú thích, hình và công thức đều là đối tượng gốc của Word.

**Kiểm tra:** 60 trang, mục lục và danh sách bảng/hình cập nhật bằng Word; trích dẫn [1]–[15] theo đúng thứ tự xuất hiện; câu gốc của DINOv3 đã đối chiếu với bài báo.

---

## Task 6 – Hoàn thiện OCR và đưa vào máy chủ (09/11/2026) ✅

**Việc đã làm:** xuất PP-OCRv5 và VietOCR sang ONNX, viết `ocr.py` (chỉnh nghiêng, gom hàng, tách trường, khớp tên), thêm `POST /v1/prescriptions/parse`, `GET /v1/catalog`.

**Kết quả test một lần:** ảnh gốc đúng hoàn toàn 99,85% dòng thuốc, 99,66% đơn; ảnh mô phỏng chụp giấy 98,93% và 97,96%. Khoảng 5 giây/đơn trên CPU.

**Giới hạn:** chưa đo trên ảnh chụp giấy thật, nên màn xác nhận vẫn bắt buộc. Chi tiết: `../archive/MediCheck_decisions.md` mục 15.

---

## Task 5 – Giao module và file ONNX cho nhóm app (08/11/2026) ✅

**Đã làm:**
- Trên repo có `backend/` (module + server), mô hình `out/onnx_final/`, [backend/API.md](../../backend/API.md) và README.
- `API.md` gồm: cách chạy máy chủ, định dạng JSON gửi/nhận, ví dụ curl, **code Dart gọi API**, hướng dẫn demo qua Wi-Fi (firewall, Android cleartext).
- Đã chạy máy chủ thật bằng uvicorn và gọi bằng curl: "Đúng hết. 5 viên khớp cữ sáng.", 1,6 giây.

**Quyết định và phản biện:**
- **Code Dart** dùng gói `image` (xoay EXIF, thu về 2048 px, JPEG q85), không dùng gói nén ảnh của hệ điều hành. Như vậy ảnh gửi lên giống đúng ảnh đã đo.
- **Tìm và sửa lỗi:**
  - viên của thuốc "chỉ nhắc lịch" từng bị báo đỏ oan, nay báo vàng;
  - gõ payload có dấu trên dòng lệnh Windows làm hỏng tên thuốc. Đã ghi lưu ý UTF-8 vào `API.md`.

**Cần bạn:** gửi link `backend/API.md` cho 2 bạn mobile.

## Task 4 – Chạy test một lần (08/11/2026) ✅

**Đã làm:**
- Ghi trước con số chính thức và đẩy lên repo (commit "Pre-register the single test-fold evaluation").
- Sau đó mới mở khóa test và chạy **một lần** qua đúng máy chủ: 1.230 cảnh, 36 phút.

**Kết quả chính thức:**
| | Test | Val |
|---|---|---|
| **Cữ đúng được báo xanh** | **90,2%** | 90,9% |
| Cận trên nhận nhầm viên ngoài đơn | **1,09%** | 1,19% |
| Cận trên nhận nhầm viên lạ | **1,31%** | 1,79% |
| Detector đếm đúng | 98,5% | 98,6% |

Cả hai chỉ số an toàn đạt chuẩn ≤ 2%; báo xanh vượt mục tiêu 70%. Test sát val, chứng tỏ cách chọn mô hình trên val không "học tủ".

**Điểm cần biết:**
- Trên test có 1,4% viên đúng bị báo đỏ oan (val 0,1%).
- Theo nguyên tắc, tôi **không chỉnh** gì dựa trên test.
- Đỏ chỉ là lời khuyên, luôn kèm "hãy kiểm vỏ hộp", và không ảnh hưởng an toàn. Đã ghi vào phần giới hạn.

---

## Task 3 – Kiểm module trên tập val (08/11/2026) ✅

**Đã làm:** cho toàn bộ 1.244 cảnh val đi đúng đường của app: ảnh 2048 px → module ONNX trên CPU, kèm các phép tráo viên lạ.

**Kết quả:**
| Đo trên val | Báo xanh | Cận trên nhận nhầm (viên ngoài đơn / viên lạ) |
|---|---|---|
| Bản PyTorch trước đây | 89,5% | 1,49% / 1,84% |
| **Module, cùng giao thức** | **91,1%** | 1,52% / 1,81% |
| **Module, ngưỡng cố định 0,0529** | **90,9%** | 1,19% / 1,79% |

- Khớp và an toàn. Module cao hơn 1,6 điểm vì máy chủ chỉ đếm số viên, còn code cũ đòi box trùng khung nhãn.
- Trên cùng dữ liệu cosine, module trùng tuyệt đối với code đánh giá.
- Tốc độ: 3 viên ≈ 0,7 giây trên CPU.

**Quyết định và phản biện:**
- **Ngưỡng đỏ "không thuộc đơn" = 0,30:** chỉ 0,31% viên đúng bị báo đỏ oan.
  - Nếu chọn 0,25 thì bắt được 85% viên lạ, nhưng báo oan 0,9%.
  - Câu "đừng uống" sai có thể làm người cao tuổi bỏ liều. Viên lạ không đỏ thì vẫn vàng, nên vẫn an toàn.
- **Đỏ "thuốc cữ khác":** bắt 95% viên nhầm cữ, báo oan ≤ 0,2%.

## Task 2 – Viết module suy luận + máy chủ API (08/11/2026) ✅

**Đã làm:**
- `backend/` gồm: module `PillVerifier` (ONNX, không cần PyTorch), server FastAPI `POST /v1/pills/verify`, tài liệu [backend/API.md](../../backend/API.md) cho nhóm mobile, 7 kiểm thử tự động (đều đạt).
- Server trả về: trạng thái từng viên, box để khoanh, câu nói, thuốc còn thiếu.

**Phát hiện quan trọng:**
- File bảng tra cũ (141 tên) lập từ **mọi fold, kể cả test**, khác bảng đã dùng khi đo.
- **Quyết định:** dùng bảng chỉ lập từ train (138 tên). Như vậy không rò rỉ test, và máy chủ đúng như lúc đo. Cái giá: 3 thuốc chỉ nhắc lịch.

**Quyết định khác:**
- AI viết cả server (theo lựa chọn của bạn).
- Kiểm chất lượng ảnh chỉ thêm lời khuyên, không bao giờ làm mất báo xanh.

---

## Task 1 – Vẽ sơ đồ các pipeline (08/11/2026) ✅

**Đã làm:** vẽ 7 sơ đồ trong `docs/diagrams/`:
1. tổng quan hệ thống;
2. kiểm thuốc khi app chạy;
3. tiền xử lý dữ liệu;
4. train và chọn mô hình;
5. đánh giá cả chuỗi;
6. OCR đơn thuốc;
7. luồng người dùng.

Các sơ đồ được nhúng cạnh phần chữ trong README, decisions, tong_hop và brainstorm, rồi push lên repo.

**Quyết định và phản biện:**
- **Định dạng: viết Mermaid (`.mmd`) rồi xuất ảnh PNG.**
  - Chỉ dùng Mermaid nhúng thẳng: GitHub hiển thị được, nhưng preview VSCode và file Word thì không.
  - Chỉ vẽ ảnh tay: khó sửa khi pipeline đổi.
  - Cách đã chọn giữ được cả hai: sửa bằng chữ, xem được ở mọi nơi, dán thẳng vào báo cáo.
- **Nội dung sơ đồ:** vẽ theo đúng logic trong code (`eval.py`), không vẽ theo ý tưởng.
- **Kiểm tra:** đã xem lại từng ảnh. Sơ đồ tổng quan ban đầu quá rộng, chữ nhỏ, nên đổi sang bố cục dọc.
