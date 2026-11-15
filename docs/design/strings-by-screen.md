# Câu chữ theo từng màn hình

> **Trả lời câu hỏi:** mỗi màn hình đang hiển thị những chuỗi chữ nào (dùng để điền `mobile/lib/core/strings_vi.dart`).
> **Sinh tự động** từ `docs/design/screens/*.html`; không sửa tay. Sửa thiết kế rồi sinh lại. Dòng `[ảnh]` và `[biểu tượng]` là nhãn cho TalkBack.
> Chuỗi có số, tên thuốc, ngày giờ là dữ liệu mẫu của bản vẽ; trong app chúng được điền từ dữ liệu thật (xem [design-spec.md](design-spec.md)).

## 1. Bắt đầu: nhập và xác nhận đơn

### SCR-WELCOME (`welcome`)

- Nghe lại
- MediCheck
- Kiểm thuốc của bác có khớp với đơn không?
- App hỗ trợ đối chiếu với đơn, không thay thế dược sĩ.
- Chọn đơn thuốc
- Thử với đơn mẫu

### SCR-IMPORT (`import`)

- Quay lại
- Nghe lại
- Chọn đơn thuốc
- Bác chọn ảnh hoặc file PDF của đơn thuốc đã khám.
- Thấy đủ cả tờ đơn
- Không bị mờ, không bị lóa
- Chữ nằm ngang, không bị nghiêng
- Chọn ảnh hoặc PDF đơn
- Chụp đơn giấy

### SCR-READING (`reading`)

- [biểu tượng] Đang tải
- Đang đọc đơn, xin chờ khoảng 10 giây.
- Ảnh đơn đang được gửi tới máy kiểm thuốc. Bác đừng thoát ra nhé.
- Hủy

### SCR-CONFIRM (`confirm`)

- Quay lại
- Nghe lại
- Đây là lịch app đọc được. Bác xem lại giúp.
- Đơn kê ngày 07/07/2020
- Bệnh: H81 - Rối loạn chức năng tiền đình ; (R51) Đau đầu
- Đơn cũ (kê ngày 18/05/2020) sẽ kết thúc khi bác tạo lịch cho đơn này.
- Hoạt huyết dưỡng não qn 150mg+20mg
- SL: 20
- Sáng 2 viên · Tối 2 viên
- Sửa
- Panactol 500mg
- SL: 10
- Sáng 1 viên · Tối 1 viên
- Đúng rồi, tạo lịch
- Gửi người thân
- Hủy

### SCR-CONFIRM – 5 kiểu thẻ (`confirm-cards`)

- Bảng tham chiếu cho SCR-CONFIRM: dòng chữ xám nhỏ là chú thích thiết kế, không hiện trong app.
- 1. needs_review (OCR chưa chắc)
- App chưa chắc dòng này, bác kiểm lại giúp
- Amoxicilin 500mg 500mg
- SL: 21
- Sáng 1 viên · Trưa 1 viên · Tối 1 viên
- Sửa
- 2. missing_schedule (đơn không có lịch)
- Vitamin c stada 1g 1g
- SL: 20
- Chưa có lịch
- Nhập theo lời dặn của bác sĩ hoặc dược sĩ.
- Chọn lịch
- Để sau
- 3. half_pill (nửa viên)
- Kavasdin 5 5mg
- SL: 15
- Sáng ½ viên
- Nửa viên – tự kiểm theo vỏ hộp
- 4. as_needed (khi cần, không nhắc giờ)
- Paracetamol 500mg 500mg
- SL: 10
- Khi cần – không nhắc giờ
- 5. name = null (ngoài danh mục: chỉ nhắc lịch)
- Thuốc không có trong danh mục
- SL: 30
- Tối 1 viên
- Chỉ nhắc lịch – app không kiểm được thuốc này bằng hình

### SCR-EDIT-LINE (`edit-line`)

- Quay lại
- Nghe lại
- Sửa thuốc
- Tên thuốc
- panactol
- Panactol 500mg
- Mypara 500 500mg
- Paracetamol 500mg 500mg
- Số viên mỗi buổi
- Sáng
- 1
- ½
- Trưa
- 0
- Chiều
- Tối
- "½" là nửa viên: app chỉ nhắc, không kiểm bằng hình.
- Xong

### SCR-PRES-CAMERA (`pres-camera`)

- [ảnh] Xem trước camera: tờ đơn thuốc
- Quay lại
- Đặt đơn lên mặt bàn, giữ máy ngang phía trên đơn. Bấm nút tròn lớn khi đơn nằm gọn trong khung.

## 2. Hằng ngày: màn chính, cữ cần uống, chụp thuốc

### SCR-HOME (`home`)

- Nghe lại
- Hôm nay
- Chủ nhật, 15/11/2026
- Cữ tiếp theo
- Cữ tối · 20:00
- 3 viên
- Uống cữ này
- Các cữ hôm nay
- Sáng · 7:00
- Đã uống 7:05
- Trưa · 11:30
- Không có thuốc
- Chiều · 17:00
- Tối · 20:00
- Sắp tới · 3 viên
- Đơn thuốc
- Lịch sử
- Cài đặt

### SCR-DOSE – cữ sáng (`dose`)

- Quay lại
- Nghe lại
- Cữ sáng · 3 viên
- Hôm nay · 7:00
- Hoạt huyết dưỡng não qn 150mg+20mg
- × 2 viên
- Panactol 500mg
- × 1 viên
- Lấy đủ các viên trên ra lòng bàn tay, rồi bấm Kiểm thuốc.
- Kiểm thuốc
- Đổi cữ

### SCR-DOSE – Đổi cữ (`dose-switch`)

- Cữ sáng · 3 viên
- Chọn cữ
- Sáng
- 3 viên · đang chọn
- Trưa
- Không có thuốc
- Chiều
- Tối
- 3 viên
- Đóng

### SCR-DOSE – đã uống (`dose-taken`)

- Quay lại
- Nghe lại
- Cữ sáng đã uống lúc 7:05.
- Đã kiểm bằng ảnh
- Hoạt huyết dưỡng não qn 150mg+20mg × 2 viên
- Panactol 500mg × 1 viên
- Về màn chính

### SCR-CAPTURE (`capture`)

- [ảnh] Xem trước camera: bàn tay có các viên thuốc
- Quay lại
- Xòe bàn tay ra, đặt thuốc lên lòng bàn tay, các viên rời nhau, rồi chụp.
- Ảnh có sẵn

### SCR-CAPTURE – chụp lại (`capture-retake`)

- [ảnh] Xem trước camera: bàn tay có viên thuốc
- Quay lại
- Chỉ để các viên còn thiếu trên tay: kavasdin 5 5mg × 1.
- Đây là lần chụp lại cuối cùng của cữ này.
- Ảnh có sẵn

### Hướng dẫn lần đầu (`guide-first-time`)

- Cách chụp thuốc
- Đang đọc to…
- [biểu tượng] Hình minh họa: bàn tay xòe với ba viên thuốc rời nhau, máy ảnh ở phía trên
- 1
- Xòe bàn tay ra.
- 2
- Đặt các viên thuốc lên lòng bàn tay, các viên rời nhau, không chồng lên nhau.
- 3
- Giữ máy phía trên, thấy rõ các viên trong khung, rồi bấm nút tròn lớn.
- Tôi hiểu rồi
- Bỏ qua

## 3. Kết quả kiểm thuốc và ghi nhận

### SCR-RESULT – xanh (`result-green`)

- Quay lại
- Nghe lại
- Đúng hết. 3 viên khớp cữ sáng.
- [ảnh] Ảnh vừa chụp: ba viên thuốc trên lòng bàn tay
- Viên này khớp panactol 500mg.
- Chạm vào từng viên để nghe lại.
- Tôi đã uống

### SCR-RESULT – đỏ, còn lượt (`result-retake`)

- Quay lại
- Nghe lại
- Có 2 viên không đúng, hãy bỏ ra.
- [ảnh] Ảnh vừa chụp: ba viên thuốc, hai viên khoanh đỏ
- Viên này là thuốc buổi tối (hoạt huyết dưỡng não qn 150mg+20mg). Đừng uống viên này trong cữ này.
- Bỏ viên này ra.
- Viên này đúng, để riêng ra.
- Chụp lại
- Tôi đã kiểm vỏ hộp

### SCR-RESULT – vàng, hết lượt (`result-final`)

- Quay lại
- Nghe lại
- Có 1 viên app chưa xác nhận được.
- [ảnh] Ảnh vừa chụp: bốn viên thuốc, một viên khoanh nét đứt
- App chưa xác nhận được viên này, hãy kiểm vỏ hộp.
- Bác đã chụp lại 1 lần rồi.
- Tôi đã kiểm vỏ hộp

### SCR-RESULT – lỗi kết nối (`result-error`)

- Quay lại
- Nghe lại
- Chưa kết nối được máy kiểm thuốc. Bác thử lại, hoặc tự kiểm theo vỏ hộp.
- Chưa có kết quả kiểm bằng hình cho cữ này.
- Thử lại
- Tôi đã kiểm vỏ hộp

### Tự kiểm vỏ hộp (`self-check`)

- Quay lại
- Nghe lại
- Hãy đối chiếu tên trên vỏ hộp với đơn.
- Cữ sáng cần các thuốc sau. Bác cầm từng hộp lên, so tên với dòng bên dưới.
- Hoạt huyết dưỡng não qn 150mg+20mg
- × 2 viên
- Panactol 500mg
- × 1 viên
- Tôi đã kiểm vỏ hộp

### SCR-DONE (`done`)

- Nghe lại
- Đã ghi nhận cữ sáng lúc 7:05.
- Tự về màn chính sau 5 giây.
- Về màn chính

## 4. Quản lý đơn, lịch sử, cài đặt, gửi người thân

### Danh sách đơn (`pres-list`)

- Quay lại
- Nghe lại
- Đơn thuốc
- Đang dùng
- Đơn kê ngày 07/07/2020
- 2 thuốc · dùng đến 19/11/2026
- Đã kết thúc
- Đơn kê ngày 18/05/2020
- 3 thuốc · kết thúc 15/11/2026
- Thêm đơn mới

### SCR-PRES-DETAIL (`pres-detail`)

- Quay lại
- Nghe lại
- Đang dùng
- Đơn kê ngày 07/07/2020
- Bệnh: H81 - Rối loạn chức năng tiền đình ; (R51) Đau đầu
- Dùng từ 15/11/2026 đến 19/11/2026
- Hoạt huyết dưỡng não qn 150mg+20mg
- SL: 20
- Sáng 2 viên · Tối 2 viên
- Sửa
- Panactol 500mg
- SL: 10
- Sáng 1 viên · Tối 1 viên
- Gửi người thân
- Kết thúc đơn
- Xóa đơn

### SCR-HISTORY (`history`)

- Quay lại
- Nghe lại
- Lịch sử 7 ngày
- Ngày
- Sáng
- Trưa
- Chiều
- Tối
- CN 15/11
- [biểu tượng] App đã kiểm
- [biểu tượng] Không có thuốc
- [biểu tượng] Chưa đến giờ
- T7 14/11
- T6 13/11
- [biểu tượng] Tự kiểm vỏ hộp
- T5 12/11
- [biểu tượng] Chưa uống
- T4 11/11
- T3 10/11
- T2 09/11
- App đã kiểm bằng ảnh
- Bác tự kiểm theo vỏ hộp
- Chưa uống
- Không có thuốc
- Chưa đến giờ

### SCR-SETTINGS (`settings`)

- Quay lại
- Nghe lại
- Cài đặt
- Giờ nhắc uống thuốc
- Sáng
- 7:00
- Trưa
- 11:30
- Chiều
- 17:00
- Tối
- 20:00
- Giọng nói
- Đọc to kết quả
- Bật
- Máy kiểm thuốc
- Địa chỉ máy chủ
- http://10.0.2.2:8000
- Kiểm tra kết nối
- Đã kết nối (final-2026-11-08)
- App hỗ trợ đối chiếu với đơn, không thay thế dược sĩ.

### SCR-SHARE – hộp cảnh báo (`share-warn`)

- Ảnh đơn có họ tên và số BHYT của bác. Chỉ gửi cho người thân tin cậy.
- Gửi
- Hủy

### SCR-SHARE – ảnh phiếu đơn (1080 px) (`share-phieu`)

- PHIẾU ĐƠN APP ĐỌC ĐƯỢC
- Đơn kê ngày 07/07/2020 · Bệnh: Tăng huyết áp vô căn (nguyên phát); Rối loạn tuần hoàn não
- Nhờ người nhà so với ẢNH ĐƠN GỐC gửi kèm.
- STT
- Tên thuốc
- SL
- Sáng
- Trưa
- Chiều
- Tối
- Ghi chú
- 1
- Kavasdin 5 5mg
- 30
- –
- 2
- Panactol 500mg
- 20
- 3
- Hoạt huyết dưỡng não bdf 150mg+5mg
- Chú thích: số = số viên mỗi lần uống · ½ = nửa viên · – = không uống
- App hỗ trợ đối chiếu với đơn, không thay thế dược sĩ.
- MediCheck

## 5. Trạng thái đặc biệt

### Màn chờ: đang kiểm thuốc (`checking`)

- [biểu tượng] Đang tải
- Đang kiểm thuốc.
- Bác chờ vài giây, giữ nguyên máy nhé.
- Hủy

### SCR-HOME – chưa có đơn (`home-empty`)

- Nghe lại
- Hôm nay
- Chủ nhật, 15/11/2026
- Chưa có đơn nào
- Bác chọn ảnh đơn thuốc để app tạo lịch uống và nhắc giờ.
- Chọn đơn thuốc
- Cài đặt

### Bị từ chối quyền camera (`camera-denied`)

- Quay lại
- Nghe lại
- App cần dùng máy ảnh để chụp thuốc.
- Bác bấm Mở cài đặt, chọn Quyền, rồi bật Máy ảnh. Hoặc bác chọn một ảnh thuốc có sẵn trong máy.
- Mở cài đặt
- Chọn ảnh có sẵn

