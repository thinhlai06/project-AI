# Thiết kế giao diện

Thư mục này là **nguồn dựng lại giao diện app** (Flutter). Bắt đầu ở [design-spec.md](design-spec.md); xem nhanh mọi màn ở [index.html](index.html) (mở bằng trình duyệt).

| File | Nội dung |
|---|---|
| [design-spec.md](design-spec.md) | Token, linh kiện, danh sách màn, cách khoanh viên trên ảnh, nhật ký review |
| [index.html](index.html) | Xem mọi màn trên một trang, bấm thử luồng |
| [strings-by-screen.md](strings-by-screen.md) | Chuỗi chữ từng màn (sinh tự động) |
| `screens/` | Mỗi màn một file HTML tĩnh; số đo nằm trong `style` |
| `png/` | Ảnh chuẩn (390 × 844) để so sánh khi dựng |
| `assets/` | Ảnh dùng trong bản vẽ |
| `screens.json` | Danh sách màn và kích thước |

## Cho người (hoặc AI) dựng màn hình

1. Mở `png/<màn>.png` và `screens/<màn>.html` của màn trong task (backlog ghi tên file ở mục "Thiết kế" của story).
2. Lấy số đo từ HTML (1 px = 1 dp), màu và chữ từ token trong [design-spec.md](design-spec.md); không viết số rời.
3. Điền câu chữ từ [strings-by-screen.md](strings-by-screen.md) vào `strings_vi.dart`.
4. Chạy trên máy giả lập 390 × 844, chụp màn hình, so với `png/`. Lệch là chưa xong.

## Khi cần sửa thiết kế

Xin chủ dự án sửa (canvas Design trên claude.ai là nơi chỉnh sửa), rồi xuất lại thư mục này. **Không sửa tay** `screens/`, `png/`, `index.html`, `strings-by-screen.md`: chúng là sản phẩm xuất ra. Ghi thay đổi vào mục 9 của design-spec.
