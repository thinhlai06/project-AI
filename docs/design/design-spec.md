# Đặc tả thiết kế giao diện (bàn giao cho lập trình)

> **Trả lời câu hỏi:** giao diện trông thế nào đến từng pixel, và dựng lại bằng Flutter ra sao để giống bản thiết kế.
> Nội dung và hành vi màn hình: [../product/ui-ux-spec.md](../product/ui-ux-spec.md). File này bổ sung **hình dáng**: màu, cỡ, khoảng cách, bố cục.
> Cập nhật: 2026-11-15 · Trạng thái: **đã chốt** (đã review UI/UX hai vòng, mục 9)

## 1. Thư mục này có gì

| File | Dùng để |
|---|---|
| [index.html](index.html) | Xem mọi màn hình trên một trang; bấm vào màn để mở bản đầy đủ, các nút đã nối sẵn để thử luồng |
| `screens/*.html` | **Nguồn dựng lại.** Mỗi màn một file HTML tĩnh, mọi giá trị nằm ngay trong `style` (không cần chạy script). Mở bằng trình duyệt hoặc đọc mã để lấy số đo |
| `png/*.png` | **Ảnh chuẩn để so sánh**, chụp ở đúng kích thước (390 × 844, một số màn cao hơn) |
| [strings-by-screen.md](strings-by-screen.md) | Mọi chuỗi chữ từng màn (sinh tự động từ HTML) để điền `strings_vi.dart` |
| `assets/` | Ba ảnh dùng trong bản vẽ (ảnh thuốc A1, A2 và đơn 582, đã thu nhỏ) |
| `screens/design-system.html` | Bảng màu, chữ, nút, biểu tượng, trạng thái viên thuốc |

Bản canvas tương tác (chủ dự án xem được trên claude.ai) chỉ là bản xem; **nguồn sự thật là thư mục này**.

## 2. Quy tắc dựng lại

1. **1 px bản vẽ = 1 dp trong Flutter**; khung điện thoại 390 × 844 dp. Màn cao hơn 844 là màn **cuộn được**; thanh nút dưới đáy luôn **cố định** (không cuộn theo nội dung).
2. Mọi màu, cỡ chữ, khoảng cách lấy từ **token** (mục 3). Không viết số màu hay cỡ chữ trực tiếp trong màn hình; thiếu token thì thêm token và ghi vào file này.
3. Mỗi màn dựng xong phải **so được với `png/<màn>.png`**: chạy trên máy giả lập 390 × 844, chụp màn hình, đặt cạnh ảnh chuẩn. Lệch bố cục, màu hay chữ là chưa xong. Màn quan trọng (xem mục 8) nên có golden test.
4. Chữ trong bản vẽ là **dữ liệu mẫu** (tên thuốc, số viên, ngày giờ). Trong app chúng đến từ database hoặc server. Câu chữ cố định lấy từ [strings-by-screen.md](strings-by-screen.md).
5. Khác thiết kế (thêm nút, đổi màu, bớt dòng) → **hỏi chủ dự án**, sửa thiết kế trước rồi mới sửa code.
6. Không dùng emoji làm biểu tượng; dùng biểu tượng ở mục 5.

## 3. Token

Đặt ở `mobile/lib/app/tokens.dart` (ST-02.1). Mã mẫu:

```dart
import 'package:material_ui/material_ui.dart';

abstract final class AppColors {
  static const bg = Color(0xFFFFFFFF);
  static const surface = Color(0xFFF4F6F9);       // thẻ, ô nhập
  static const text = Color(0xFF111111);           // 18,9:1 trên nền trắng
  static const textStrong2 = Color(0xFF4A4F57);    // chữ trên nút bị khóa, nhãn tag
  static const muted = Color(0xFF5F6672);          // chữ phụ, 5,8:1
  static const outline = Color(0xFF767C86);        // viền nút/ô nhập, 4,2:1
  static const divider = Color(0xFFDDE1E7);        // chỉ trang trí
  static const primary = Color(0xFF0B57D0);        // chữ trắng trên nền này 6,4:1
  static const primaryTint = Color(0xFFE8F0FE);
  static const green = Color(0xFF187038);          // chữ trắng 6,2:1
  static const greenTint = Color(0xFFE6F4EA);
  static const yellow = Color(0xFF8F5600);         // chữ trắng 6,0:1; trên yellowTint 5,5:1
  static const yellowTint = Color(0xFFFFF4D6);
  static const red = Color(0xFFB3261E);            // chữ trắng 6,5:1
  static const redTint = Color(0xFFFCE8E6);
  static const overlayYellow = Color(0xFFFFD479);  // CHỈ nét đứt khoanh viên vàng trên ảnh
  static const scrimCamera = Color(0xD1000000);    // đen 82%: thanh chữ/thanh nút trên camera
  static const scrimFrame = Color(0x73000000);     // đen 45%: vùng ngoài khung chụp
  static const scrimDialog = Color(0x8C000000);    // đen 55%: nền sau hộp thoại
  static const scrimSheet = Color(0x80000000);     // đen 50%: nền sau bảng chọn cữ
  static const scrimGuide = Color(0xB3000000);     // đen 70%: nền sau hướng dẫn lần đầu
}

abstract final class AppText {
  static const _f = 'Roboto';                     // font mặc định của Android; iOS dùng font hệ thống
  static const huge = TextStyle(fontFamily: _f, fontSize: 34, height: 40 / 34, fontWeight: FontWeight.w700);
  static const title = TextStyle(fontFamily: _f, fontSize: 28, height: 34 / 28, fontWeight: FontWeight.w700);
  static const cardTitle = TextStyle(fontFamily: _f, fontSize: 24, height: 30 / 24, fontWeight: FontWeight.w700);
  static const button = TextStyle(fontFamily: _f, fontSize: 22, height: 28 / 22, fontWeight: FontWeight.w700);
  static const bodyStrong = TextStyle(fontFamily: _f, fontSize: 20, height: 28 / 20, fontWeight: FontWeight.w700);
  static const bodyMedium = TextStyle(fontFamily: _f, fontSize: 20, height: 28 / 20, fontWeight: FontWeight.w500);
  static const body = TextStyle(fontFamily: _f, fontSize: 20, height: 28 / 20, fontWeight: FontWeight.w400);
}

abstract final class AppSpace {
  static const s = 8.0, m = 16.0, l = 24.0;       // lề màn hình = 16
  static const touchMin = 48.0;
  static const primaryButtonHeight = 64.0, secondaryButtonHeight = 56.0, appBarHeight = 56.0;
  static const radiusButton = 16.0, radiusCard = 16.0, radiusField = 12.0, radiusBox = 10.0;
}
```

Từ ST-01 dự án dùng `package:material_ui/material_ui.dart` (ADR-019); `package:flutter/material.dart` đã deprecated.

- Cỡ chữ người dùng phải đọc **không nhỏ hơn 20**. Chỉ có hai ngoại lệ: chữ trong bảng phiếu đơn gửi người thân (≥ 32 trên ảnh rộng 1080 px) và các chú thích thiết kế (không có trong app).
- Chữ hệ thống phóng tới **1,5 lần** (`textScaler` chặn ở 1,5); bố cục phải xuống dòng, không cắt chữ.
- Không dùng `muted` trên `divider` (4,4:1). Mọi cặp chữ/nền còn lại của bảng màu đều ≥ 4,5:1.
- Màu là **một trong bốn dấu hiệu** của trạng thái (màu + biểu tượng + kiểu nét + chữ); xem mục 7.

## 4. Linh kiện dùng chung

| Linh kiện | Số đo | Ghi chú |
|---|---|---|
| `PrimaryButton` | cao 64, rộng hết bề ngang, góc 16, nền `primary`, chữ `button` trắng, icon 28 (nếu có) cách chữ 10 | Một nút chính mỗi màn. Khóa: nền `divider`, chữ `textStrong2`, kèm câu giải thích ngay trên nút |
| `SecondaryButton` | cao 56, viền 2 `primary`, chữ `button` màu `primary`, nền trắng | Hai nút phụ cạnh nhau: `Row`, mỗi nút `Expanded`, cách nhau 12, chữ 20 |
| `DangerButton` | như `SecondaryButton`, viền và chữ `red` | Luôn hỏi lại 2 bước |
| `AppBar` tự dựng | cao 56; trái: "‹ Quay lại" (cao 48, chữ 20/500 `primary`); phải: nút "Nghe lại" (🔊 + chữ, cao 48) | WELCOME, HOME, DONE chỉ có "Nghe lại" |
| `BottomBar` | đệm 16, nền trắng, đường kẻ `divider` 1 dp phía trên, các nút cách nhau 12 | Cố định ở đáy; nội dung cuộn phía trên |
| `AppCard` | nền `surface`, góc 16, đệm 16, các dòng cách 8 | Thẻ cần chú ý: nền `yellowTint` (kèm biểu tượng + câu) |
| `Tag` | cao 36, góc 18, đệm ngang 12, chữ 20/700; "Đang dùng" nền `primary` chữ trắng + dấu tích; "Đã kết thúc" viền 2 `outline` | |
| `Stepper` | nút − và + 56 × 56 (viền 2 `primary`, góc 16, biểu tượng 28), số 34 giữa (rộng 44), nút "½" 56 × 56 tròn viền `outline` | Số bằng 0: nút − viền `divider`, số màu `muted` |
| `Field` | cao 56, viền 2 `outline`, góc 12, đệm ngang 14, chữ 20 | Chỉ dùng cho ô tìm thuốc và địa chỉ server |
| `Switch` | 72 × 44, núm tròn 36, nền `primary` khi bật; luôn kèm chữ Bật/Tắt | Hàng chứa nó cao ≥ 72 |
| `Spinner` | vòng 104, nét 10, nền `divider`, cung `primary` | Tĩnh trong bản vẽ; app dùng `CircularProgressIndicator` cùng màu và cỡ |
| `StatusCircle` | tròn 64 (kết quả), 112 (trạng thái lớn); nền màu trạng thái; biểu tượng trắng 38 / 64 | Xanh ✓, vàng ?, đỏ ✗; trạng thái trung tính (lỗi, quyền) dùng nền tint + biểu tượng màu |
| `PillResultRow` | thẻ góc 16, đệm 12, nền `surface` (nền tint theo trạng thái khi hàng đang được chọn hoặc cần chú ý); **ô ảnh 72 × 72** góc 14, viền theo trạng thái (xanh liền 4, vàng đứt 4, đỏ liền 6; hàng đỏ viền 6 nên ô 76); tên 20/700 (xuống dòng được), "× n viên" 20/500, dòng trạng thái 20/700 có biểu tượng 22 + chữ màu trạng thái; dòng phụ 20/500 cùng màu ("Bỏ viên này ra.", "Để riêng ra.") | Một ảnh mỗi thuốc. Hàng thiếu: ô không ảnh viền đứt `yellow`, biểu tượng viên thuốc. Không có nút sửa |
| `Callout` | thẻ tint theo trạng thái, đệm 14 × 16, biểu tượng 🔊 28 + câu 20/700 | Hiện `message` của viên đang chọn; chạm viên thì đọc `message` |
| `Scaffold` màn | nền trắng, lề ngang 16, nội dung cách 16 | |

## 5. Biểu tượng

Nét 2,2 (2,4 trong nút −/+ và dấu tích lớn), đầu nét tròn, lưới 24. Bảng đầy đủ và tên Material Icons tương ứng ở [screens/design-system.html](screens/design-system.html) (mục 4). Dùng `Icon(Icons.xxx_outlined)`; **không** thêm gói icon. Biểu tượng chỉ trang trí thì `excludeFromSemantics`. Nút tròn quen thuộc (chụp) có `Semantics(label: ...)`.

Biểu tượng tự vẽ không có trong Material (nếu muốn giống hệt, dùng `CustomPainter`/SVG nhỏ): hình bàn tay + viên thuốc ở "Hướng dẫn lần đầu" (`guide-first-time.html`), hình tờ đơn ở `import.html`. Chúng chỉ minh họa; có thể thay bằng `Icon` lớn nếu tốn công, miễn ghi lại ở đây.

## 6. Danh sách màn hình

| Màn | File | SCR / story | Cao (dp) | Ghi chú dựng |
|---|---|---|---|---|
| Chào | `welcome` | SCR-WELCOME · ST-06.1 | 844 | Nút dưới đáy; nội dung giữa màn |
| Chọn nguồn đơn | `import` | SCR-IMPORT · ST-06.1 | 844 | |
| Đang đọc đơn | `reading` | SCR-READING · ST-06.2 | 844 | Không có AppBar; chỉ có "Hủy" |
| Xác nhận đơn | `confirm` | SCR-CONFIRM · ST-07.2 | 900 | Cuộn; BottomBar cố định: nút chính + hai nút phụ cạnh nhau. Banner vàng chỉ khi đã có đơn đang dùng |
| 5 kiểu thẻ thuốc | `confirm-cards` | SCR-CONFIRM · ST-07.2 | 1330 | Bảng tham chiếu, **không phải màn**; dòng chữ xám nhỏ là chú thích thiết kế |
| Sửa dòng | `edit-line` | SCR-EDIT-LINE · ST-07.3 | 920 | Danh sách gợi ý theo ô tìm; dòng đang chọn nền `primaryTint` + viền `primary` + dấu tích |
| Chụp đơn giấy | `pres-camera` | SCR-PRES-CAMERA · ST-19.1 | 844 | Khung viền trắng 4 dp, vùng ngoài khung tối 45% |
| Hôm nay | `home` | SCR-HOME · ST-09.1 | 900 | Thẻ cữ tiếp theo nền `primaryTint`, nút chính nằm trong thẻ; ba liên kết đáy cao ≥ 72 |
| Hôm nay (chưa có đơn) | `home-empty` | SCR-HOME · ST-09.1 | 844 | Trạng thái rỗng |
| Cữ cần uống | `dose` | SCR-DOSE · ST-11.2 | 844 | Số viên cỡ `huge` |
| Đổi cữ | `dose-switch` | SCR-DOSE · ST-11.2 | 844 | Bảng chọn từ đáy, góc trên 24; ô 88 cao; cữ không có thuốc không bấm được |
| Cữ đã uống | `dose-taken` | SCR-DOSE · ST-11.3 | 844 | Dấu tích **xanh dương** (đã ghi nhận), không phải xanh lá (xanh lá chỉ dành cho viên khớp) |
| Chụp thuốc | `capture` | SCR-CAPTURE · ST-12.1 | 844 | **Khung ngắm** 342 × 380 (trái 24, cách đỉnh 235): bốn góc chữ L 36 dp nét 5 dp góc bo 12; dấu + 40 × 4 ở giữa (tâm 195, 425); vùng ngoài tối 45%. Thanh dưới cao 144: "Ảnh có sẵn" 112 × 68 (trái 16), nút chụp 88 (giữa), "Hướng dẫn" 112 × 68 (phải) |
| Chụp lại | `capture-retake` | SCR-CAPTURE · ST-14.2 | 844 | Câu hướng dẫn có tên thuốc còn thiếu |
| Hướng dẫn lần đầu | `guide-first-time` | ST-17.1 | 844 (mở lại bằng nút "Hướng dẫn") | Thẻ trắng góc 24 trên nền camera tối 70% |
| Đang kiểm thuốc | `checking` | ST-13.2 | 844 | Có "Hủy" |
| Kết quả xanh | `result-green` | SCR-RESULT · ST-13.2/13.3/29.3 | 940 | Chỉ ở đây có "Tôi đã uống". Cuộn; thanh nút cố định |
| Kết quả đỏ, còn lượt | `result-retake` | SCR-RESULT · ST-14.2/29.3 | 1150 | Dòng phụ trong từng hàng thay cho chú giải: "Bỏ viên này ra." / "Để riêng ra." |
| Kết quả vàng, hết lượt | `result-final` | SCR-RESULT · ST-13.3/29.3 | 1090 | Chỉ còn "Tôi đã kiểm vỏ hộp". Hàng "Viên chưa xác nhận" lên đầu |
| Kết quả còn thiếu | `result-missing` | SCR-RESULT · ST-13.3/29.3 | 1030 | Cữ `not_green` do `missing[]`: hàng thuốc thiếu (không ảnh) lên đầu; còn lượt nên có "Chụp lại" |
| Lỗi kết nối | `result-error` | SCR-RESULT · ST-13.1 | 844 | Không có ảnh; "Thử lại" là nút chính |
| Tự kiểm vỏ hộp | `self-check` | UC-08 · ST-15.2 | 844 | Danh sách chữ to; biểu tượng ô tích chỉ minh họa |
| Đã ghi nhận | `done` | SCR-DONE · ST-15.1 | 844 | Tự về HOME sau 5 giây |
| Danh sách đơn | `pres-list` | ST-09.2 | 844 | Đơn đang dùng nền `primaryTint`; đã kết thúc nền `surface` |
| Chi tiết đơn | `pres-detail` | SCR-PRES-DETAIL · ST-09.2/09.3 | 1010 | "Kết thúc đơn" và "Xóa đơn" cạnh nhau |
| Lịch sử | `history` | SCR-HISTORY · ST-18.1 | 960 | Lưới: cột ngày 104, bốn cột cữ 62; hàng cao 56 cách 6; hôm nay nền `primaryTint` |
| Cài đặt | `settings` | SCR-SETTINGS · ST-04.3/18.2 | 1020 | |
| Cảnh báo gửi người thân | `share-warn` | SCR-SHARE · ST-21.3 | 844 | Hộp thoại giữa màn, rộng 342, góc 24 |
| Ảnh phiếu đơn | `share-phieu` | SCR-SHARE · ST-21.2 | 860 | **Ảnh 1080 px xuất ra PNG**, không phải màn hình. Chiều cao theo nội dung |
| Quyền camera bị từ chối | `camera-denied` | ST-12.1 | 844 | Luôn có lối thoát: "Chọn ảnh có sẵn" |

Mỗi màn có `<title>` và biểu tượng có `aria-label`/`aria-hidden`: đó là gợi ý cho `Semantics` (nhãn tiếng Việt) và `excludeSemantics`.

## 7. Khoanh viên thuốc trên ảnh kết quả

Áp dụng cho `result-green`, `result-retake`, `result-final`; dữ liệu mẫu lấy từ phản hồi **thật** của server (D1, kịch bản đỏ, D4).

- **Vùng ảnh:** rộng 358 (hết lề), cao **300**, góc 16, cắt phần thừa (`ClipRRect`). Ảnh **phóng tới vùng quanh các viên**: lấy hộp bao của mọi `pills[].box`, nới mỗi cạnh 30% (tức nhân 1,6), mở rộng cho đúng tỉ lệ 358 : 300, giữ trong ảnh. Rồi `scale = 358 / chiều rộng vùng (px ảnh)`.
- **Toạ độ hộp:** `box = [x1, y1, x2, y2]` theo tỉ lệ 0–1 của **ảnh đã gửi** (sau khi xoay EXIF). Vị trí trên màn = `offset + box × kích thước ảnh sau khi phóng`.
- **Nét hộp** (góc bo 10, xem bảng ở design-system):

| Trạng thái | Nét | Màu nét trên ảnh | Huy hiệu góc trên trái |
|---|---|---|---|
| green | liền 4 | `green` | vuông 26 nền `green`, dấu ✓ trắng |
| yellow | **đứt** 4 | `overlayYellow` (vàng nhạt, vì `yellow` chìm trên da và viên tối) | vuông 26 nền `yellow`, dấu ? trắng |
| red | liền **dày 6** | `red` | vuông 28 nền `red`, dấu ✗ trắng |

- **Viên đang chọn** (vừa chạm): thêm viền trắng 3 dp bên ngoài; `Callout` bên dưới hiện `message` của viên đó và đọc to. Mặc định chọn viên **đỏ đầu tiên**, nếu không có thì viên vàng, nếu không thì viên đầu tiên.
- **Vùng chạm:** nếu hộp nhỏ hơn 48 × 48 thì mở rộng vùng chạm (không mở rộng nét vẽ).
- **Thứ tự vẽ:** xanh → vàng → đỏ (đỏ nằm trên cùng để không bị che).
- **Ảnh viên trong danh sách** (`PillResultRow`): cắt từ ảnh đã gửi theo `box`, ô vuông có cạnh = max(rộng, cao) × 1,25 quanh tâm viên, kẹp trong ảnh, thu về 160 px (hiển thị 64 dp). Mỗi thuốc một ảnh (viên đại diện: viên có trạng thái nặng nhất của thuốc đó); số viên đã có ở chữ. Chỉ ở RAM, bỏ khi rời màn ([ADR-018](../architecture/adr/pill-crops-in-memory.md)).
- Chỉ hiện chú giải trạng thái **đang có** trong ảnh (ví dụ màn đỏ chỉ giải thích đỏ và xanh).

## 8. Hành vi mà ảnh tĩnh không thể hiện

| Việc | Cách làm |
|---|---|
| Thanh dưới đáy | `Scaffold.bottomNavigationBar` hoặc `Column` + `Expanded` + `SingleChildScrollView`; nội dung cuộn, thanh nút đứng yên |
| Đọc to | Khi mở màn: đọc câu chính (tiêu đề hoặc `summary`) nếu `tts_enabled`; nút "Nghe lại" đọc lại toàn bộ nội dung chính |
| Tự về màn chính | SCR-DONE: sau 5 giây `context.go('/')`; bấm "Về màn chính" thì về ngay |
| Màn chờ | Chặn bấm lặp; "Hủy" hủy yêu cầu mạng; quá hạn (30 s đọc đơn, 20 s kiểm thuốc) thì chuyển sang màn lỗi |
| Bàn phím | Chỉ ô tìm thuốc và địa chỉ server; khi bàn phím mở, BottomBar đẩy lên theo `viewInsets` |
| Hết lượt chụp lại | Nút "Chụp lại" biến mất; chỉ còn "Tôi đã kiểm vỏ hộp" |
| Máy thiếu giọng tiếng Việt | Hiện hướng dẫn cài giọng (câu ở `ui-ux-spec.md`), app vẫn dùng được không có giọng |
| Golden test | Làm cho: `welcome`, `confirm`, `dose`, `result-green`, `result-retake`, `result-final`, `result-error`, `share-phieu` (so với ảnh dựng bằng widget, dung sai nhỏ) |

## 9. Nhật ký review UI/UX

**Vòng 1 (xem ảnh chụp từng màn, đo tương phản, kiểm kích thước):** phát hiện và đã sửa:

| # | Phát hiện | Cách xử lý |
|---|---|---|
| 1 | Token vàng `#B26A00` chỉ đạt 3,9:1 trên nền vàng nhạt, 4,2:1 với chữ trắng: **dưới 4,5:1** (NFR-04) | Đổi thành `#8F5600` (6,0:1 và 5,5:1). Xanh `#1B7F3B` đổi `#187038` vì 4,5:1 trên nền xanh nhạt là sát ngưỡng |
| 2 | Nét vàng đậm khoanh viên chìm trên da tay và viên tối | Thêm `overlayYellow #FFD479` chỉ cho nét đứt; huy hiệu vẫn dùng màu token |
| 3 | Khung chụp chưa ôm đủ viên; khung đơn trắng trên nền đơn trắng không thấy | Căn lại ảnh/khung; thêm lớp tối 45% ngoài khung |
| 4 | Ảnh kết quả (260 cao) nhỏ, khó chạm, để trống nhiều | Tăng lên 300 và phóng theo hộp bao các viên (mục 7) |
| 5 | Hướng dẫn lần đầu: tiêu đề và "Đang đọc" bị xuống dòng chật | Xếp dọc |
| 6 | Lịch sử thiếu chú giải "Chưa đến giờ" | Thêm |
| 7 | Phiếu đơn: cột "Ghi chú" quá hẹp cho "Sau khi ăn" | Rộng 204 |
| 8 | Thiếu màn: **đang kiểm thuốc**, **chưa có đơn**, **bị từ chối quyền camera** (đặc tả có, thiết kế chưa) | Thêm 3 màn |
| 9 | Icon "mất mạng" khó nhận ra | Vẽ lại hình đám mây gạch chéo |
| 10 | "Quay lại" ở màn xác nhận trỏ về màn chờ (vô nghĩa) | Trỏ về chọn nguồn đơn |

**Vòng 2:** chụp lại và xem các màn đã sửa; không còn lỗi bố cục. Kiểm tự động: **không có chữ nhỏ hơn 20 px** ở màn hình ứng dụng; mọi vùng chạm ≥ 48; mỗi màn tối đa một nút chính; mọi cặp chữ/nền đạt ≥ 4,5:1.

**Vòng 3 (sau thảo luận với chủ dự án, 15/11):**

| # | Quyết định | Thay đổi |
|---|---|---|
| 11 | Khung ngắm kiểu bốn góc chữ L + dấu +, rộng hơn (342 × 380) để người cao tuổi khó để viên ra ngoài khung | `capture`, `capture-retake`, `pres-camera` giữ khung cũ (đơn giấy) |
| 12 | Thêm nút "Hướng dẫn" ở màn chụp | Thanh dưới có ba nút |
| 13 | Bỏ ảnh mẫu VAIPE; sau kết quả hiện ảnh viên cắt từ ảnh vừa chụp, mỗi thuốc một ảnh, không lưu gì | Danh sách "Thuốc theo kết quả" ở 4 màn kết quả; thêm màn `result-missing`; ADR-018 |
| 14 | Danh sách không cho sửa tên/số viên (giữ BR-01) | Không có ô sửa trong `PillResultRow` |

**Điểm còn mở (không chặn việc code):**
- Hình minh họa bàn tay và tờ đơn là nét đơn giản tự vẽ; có thể thay bằng hình đẹp hơn sau.
- Chưa có chế độ tối (theo PRD là giai đoạn 2).
- Tên thuốc hiển thị viết hoa chữ đầu (`Panactol 500mg`) chỉ để hiển thị; chuỗi gửi server và `message` của server vẫn giữ nguyên chữ thường ([ui-ux-spec.md](../product/ui-ux-spec.md) mục 5).
- Màn kết quả `partial` (cữ có thuốc chỉ nhắc lịch) dùng bố cục như `result-green` nhưng nút chính là "Tôi đã kiểm vỏ hộp" và không có nút "Tôi đã uống"; chưa có bản vẽ riêng vì chưa có phản hồi `partial` thật làm mẫu (server trả `not_green` khi có `unchecked_count`). Dựng theo bảng nút ở ui-ux-spec; thử với server thật khi làm ST-13.
- Các màn kết quả cao hơn 844 dp vì có danh sách: người dùng cuộn, thanh nút ở đáy luôn thấy.
