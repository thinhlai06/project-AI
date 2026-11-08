# Báo cáo công việc (mới nhất ở trên)

Mỗi phần việc có một báo cáo ngắn khoảng 100 từ. Phân tích chi tiết từng quyết định nằm ở `MediCheck_decisions.md`.

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
- `backend/` gồm: module `PillVerifier` (ONNX, không cần PyTorch), server FastAPI `POST /v1/pills/verify`, tài liệu [backend/API.md](backend/API.md) cho nhóm mobile, 7 kiểm thử tự động (đều đạt).
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
