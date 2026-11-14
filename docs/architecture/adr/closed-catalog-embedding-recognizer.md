# ADR-005: Danh mục đóng + bộ nhận dạng embedding

- **Trạng thái:** Đã chấp nhận
- **Ngày:** 2026-11-03
- **Người quyết:** phụ trách AI

## Bối cảnh

VAIPE có 107 lớp viên và 141 tên thuốc từ một hệ thống bệnh viện; không được gán nhãn tay hay thu thập dữ liệu mới. Lớp 107 là "viên không thuộc đơn", gồm cả viên của lớp đã biết.

## Quyết định

Prototype trên **danh mục đóng VAIPE**. Bộ nhận dạng xuất embedding + đầu cosine 107 lớp; quyết định theo **tập lớp được phép của đơn** (từ tên thuốc qua bảng tra), không phân loại đóng tự do. Thuốc ngoài danh mục chỉ nhắc lịch.

## Phương án đã cân nhắc

| Phương án | Vì sao không chọn |
|---|---|
| "Làm quen" 1–3 ảnh mỗi thuốc (enrollment) | Đúng trong ứng viên 80–84%, kém danh mục (93,1%) trên 400 đơn; để giai đoạn 2 |
| Phân loại đóng 107 lớp, lấy lớp cao nhất | Không tận dụng được đơn; viên ngoài đơn dễ bị gán nhầm vào lớp đã biết |

## Hệ quả

- Kiểm tốt trong danh mục; thuốc mới hoàn toàn chỉ nhắc lịch.
- Giới hạn phải khai báo: một hệ thống bệnh viện, không kiểm hàm lượng.
