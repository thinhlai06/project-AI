# Báo cáo công việc (mới nhất ở trên)

Mỗi phần việc có một báo cáo ngắn khoảng 100 từ. Phân tích chi tiết từng quyết định nằm ở `MediCheck_decisions.md`.

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
