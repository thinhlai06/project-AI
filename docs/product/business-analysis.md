# Phân tích nghiệp vụ (BA)

> **Trả lời câu hỏi:** vì sao làm MediCheck, cho ai, giải quyết vấn đề gì, trong giới hạn nào.
> **Không chứa:** yêu cầu chi tiết (xem [prd.md](prd.md)), thiết kế màn hình (xem [ui-ux-spec.md](ui-ux-spec.md)).
> Cập nhật: 2026-11-15 · Trạng thái: **đã chốt**

## 1. Bối cảnh và vấn đề

Người từ 45 tuổi trở lên, nhất là người cao tuổi mắt kém, thường uống nhiều loại thuốc mỗi ngày theo đơn bảo hiểm y tế (BHYT). Ba lỗi hay gặp:

| # | Lỗi | Hậu quả |
|---|---|---|
| P1 | Lấy nhầm thuốc không có trong đơn | Quá liều, trùng hoạt chất, phản ứng chéo |
| P2 | Uống nhầm cữ (thuốc tối uống buổi sáng) hoặc sai số viên | Sai liều, giảm hiệu quả điều trị |
| P3 | Quên đã uống hay chưa, uống lặp | Quá liều |

Ngoài ra người bệnh thường **phụ thuộc người thân** để chia thuốc, và khó đọc chữ nhỏ trên đơn và vỏ hộp.

## 2. Giải pháp tóm tắt

Ứng dụng điện thoại đối chiếu **đơn thuốc → lịch uống theo buổi → viên thuốc thực tế trên tay** chỉ bằng thao tác chụp:

1. Nhập đơn (chọn ảnh/PDF đơn, hoặc chụp đơn giấy) → AI đọc đơn → người dùng xác nhận → app tạo lịch uống.
2. Đến giờ, app nhắc bằng thông báo và giọng nói.
3. Người dùng đặt các viên của cữ lên lòng bàn tay rồi chụp → app khoanh từng viên **xanh** (khớp đơn), **đỏ** (sai cữ hoặc ngoài đơn), **vàng** (chưa chắc, hãy kiểm vỏ hộp), báo thiếu/thừa.
4. Người dùng bấm "Tôi đã uống" → app chống uống lặp.

Định vị: **công cụ hỗ trợ, không thay thế dược sĩ**. Câu chữ luôn là "khớp với đơn", không bao giờ "an toàn để uống".

## 3. Các bên liên quan

| Bên | Vai trò | Quan tâm chính |
|---|---|---|
| Người dùng cao tuổi (persona: bác Lan, 68 tuổi) | Người dùng chính, tự sử dụng | Dễ dùng, chữ to, nghe được, không sợ "bấm hỏng" |
| Người thân | Nhận đơn đã đọc để kiểm hộ (qua chia sẻ của hệ điều hành) | Đơn đọc đúng chưa |
| Nhóm dự án (3 người: 1 AI, 2 mobile) | Xây dựng và trình bày | Kịp hạn cuối 12/2026, demo thuyết phục |
| Giảng viên, hội đồng chấm | Đánh giá môn học | Tính đúng của AI, đo lường trung thực, sản phẩm chạy được |

Chưa làm: chế độ người thân theo dõi từ xa, tài khoản người dùng, kết nối bệnh viện/nhà thuốc.

## 4. Mục tiêu và chỉ số thành công

| Mã | Mục tiêu | Chỉ số | Mức đạt | Hiện trạng |
|---|---|---|---|---|
| G1 | Báo xanh đáng tin | Cận trên 95% tỉ lệ báo xanh nhầm khi có viên lạ | ≤ 2% (không nới) | **Đạt** trên test: 1,09% / 1,31% |
| G2 | Báo xanh đủ thường xuyên để có ích | Tỉ lệ cữ đúng được báo xanh | ≥ 70% | **Đạt** trên test: 90,2% |
| G3 | Đọc đơn đúng | Dòng thuốc đúng hoàn toàn (tên + số lượng + lịch) | ≥ 95% trên ảnh/PDF đơn | **Đạt** trên test: 99,85% (ảnh gốc) |
| G4 | Dùng nhanh mỗi cữ | Số chạm từ thông báo đến "Tôi đã uống" khi xanh | ≤ 3 chạm | Chưa làm app |
| G5 | Phản hồi nhanh | Thời gian từ bấm chụp đến câu kết quả | ≤ 3 giây (cữ 4 viên, laptop demo) | Server ~1–2 giây; chưa đo trên laptop demo |
| G6 | Demo trọn vẹn | Chạy đủ luồng nhập đơn → nhắc → chụp → kết quả → đã uống trên máy demo | 100% kịch bản demo | Chưa làm app |

## 5. Phạm vi

### 5.1. Trong phạm vi (MVP môn học)

- Nhập đơn BHYT bệnh viện (2 mẫu đơn của VAIPE): chọn ảnh/PDF là đường chính, chụp giấy là đường phụ.
- Màn xác nhận đơn bắt buộc, sửa bằng cách chọn (không gõ).
- Lịch uống 4 buổi (sáng, trưa, chiều, tối), nhắc cục bộ, đọc giọng nói tiếng Việt.
- Kiểm thuốc theo cữ (chế độ B: chụp tất cả viên của cữ cùng lúc), 3 trạng thái, khoanh trên ảnh, chụp lại tối đa 1 lần.
- "Tôi đã uống", "Tôi đã kiểm vỏ hộp", chống uống lặp, lịch sử.
- Chế độ "Thử với đơn mẫu" để demo.

### 5.2. Ngoài phạm vi (giai đoạn 2)

Làm quen thuốc mới (enrollment), tương tác thuốc (DDInter), chế độ người thân, chạy mô hình trên điện thoại, tự động chụp, kiểm hàm lượng, đơn ngoài 2 mẫu VAIPE, tài khoản và đồng bộ đám mây.

## 6. Ràng buộc

| Mã | Ràng buộc | Nguồn |
|---|---|---|
| C1 | Nhóm 3 người, hạn cuối 12/2026 | Môn học |
| C2 | Chỉ dùng dataset sẵn có: không gán nhãn tay, không thu thập mới, không dùng bộ định danh thuốc nước ngoài | Quyết định nhóm 2026-11-03 |
| C3 | Danh mục đóng: 138 tên thuốc kiểm được bằng hình (bảng tra chỉ lập từ tập train), 107 lớp viên | [ai/model-card.md](../ai/model-card.md) |
| C4 | Không có server thật, không có ngân sách cloud: AI chạy trên laptop khi demo | [ADR-004](../architecture/adr/laptop-demo-server.md) |
| C5 | Nhóm chỉ có iPhone, không có máy Mac và máy Android: demo chính trên máy giả lập Android | [ADR-002](../architecture/adr/flutter-android-first.md) |
| C6 | Tập test đã dùng một lần (pill 08/11, OCR 09/11): không chạy lại, không chỉnh theo test | [ADR-008](../architecture/adr/safety-rule-and-sealed-test.md) |
| C7 | Giấy phép: YOLO26/Ultralytics AGPL-3.0, DINOv3 License, bộ bổ trợ CC BY-NC-SA 4.0 (không thương mại) | [ai/model-card.md](../ai/model-card.md) |

## 7. Giả định

| Mã | Giả định | Nếu sai thì |
|---|---|---|
| A1 | Người dùng có đơn dạng ảnh/PDF hoặc đơn giấy in rõ | Chụp giấy chưa đo trên ảnh thật; màn xác nhận là lưới an toàn |
| A2 | Người dùng tự đặt được 2–5 viên rời nhau trên lòng bàn tay | Hướng dẫn bằng giọng nói lúc đầu, cho chụp lại 1 lần |
| A3 | Điện thoại và laptop nối được với nhau trong buổi demo | Phát hotspot từ điện thoại hoặc dùng tunnel ([deployment.md](../architecture/deployment.md)) |
| A4 | Máy giả lập Android có giọng đọc tiếng Việt | Cài gói giọng Google TTS tiếng Việt; nếu không có thì hiện chữ to |

## 8. Rủi ro

| Mã | Rủi ro | Khả năng | Ảnh hưởng | Cách giảm |
|---|---|---|---|---|
| R1 | Báo xanh nhầm (lỗi nguy hiểm nhất) | Thấp (đã đo ≤ 2%) | Rất cao | Ngưỡng cố định, app không bao giờ tự suy ra xanh, câu chữ "khớp với đơn" |
| R2 | Demo trên máy giả lập kém thuyết phục | Cao | Trung bình | Dùng webcam laptop làm camera; thêm cài thử lên iPhone nếu mượn được máy Mac ([ADR-002](../architecture/adr/flutter-android-first.md)) |
| R3 | Laptop trình bày chạy chậm | Trung bình | Trung bình | Đo sớm (cổng 22/11), giảm luồng hoặc đổi máy |
| R4 | Mạng phòng trình bày chặn kết nối | Trung bình | Cao | Hotspot điện thoại, tunnel HTTPS, máy giả lập gọi `10.0.2.2` trên chính laptop |
| R5 | OCR đọc sai lịch trên ảnh chụp giấy thật | Trung bình | Cao | Màn xác nhận bắt buộc, dòng kém tin cậy tô nổi |
| R6 | Trễ tiến độ app (2 người, 6 tuần) | Trung bình | Cao | Ưu tiên luồng lõi ([roadmap.md](roadmap.md)), cắt tính năng "nên có" trước |
| R7 | Lộ dữ liệu sức khỏe | Thấp | Cao | Không lưu ảnh thuốc, không lưu họ tên/số BHYT dạng chữ, server không có database; ảnh đơn chỉ ở bộ nhớ riêng của app và người dùng được nhắc trước khi gửi ảnh đơn |
| R8 | Báo đỏ oan viên đúng (1,40% trên test) làm người dùng bỏ liều | Thấp | Trung bình | Đỏ luôn kèm "hãy kiểm vỏ hộp"; khai báo trong giới hạn |

## 9. Quy tắc nghiệp vụ cốt lõi

Mọi tài liệu khác phải tuân theo các quy tắc này. Muốn đổi thì phải viết ADR mới.

| Mã | Quy tắc |
|---|---|
| BR-01 | App **chỉ** báo cữ xanh khi server trả `status = green`. App không tự suy ra xanh; mất mạng hay lỗi thì không bao giờ xanh |
| BR-02 | Mọi đơn phải qua màn xác nhận trước khi tạo lịch |
| BR-03 | Thuốc không có trong danh mục (OCR trả `name = null`) chỉ được nhắc lịch, không chấm bằng ảnh |
| BR-04 | Liều nửa viên: nhắc lịch, không chấm ảnh. Liều "khi cần": chỉ hiển thị, không nhắc |
| BR-05 | Đơn thiếu lịch: không tự suy liều; chỉ khóa dòng đó cho đến khi người dùng chọn lịch |
| BR-06 | "Trước/sau ăn": hiển thị và đọc nguyên văn, không đổi giờ nhắc |
| BR-07 | Không mô tả màu viên, không đoán "có thể là thuốc Z" |
| BR-08 | Chụp lại tối đa 1 lần mỗi cữ; viên đã xanh giữ xanh; sau đó vẫn chưa xanh thì dẫn tới "Tôi đã kiểm vỏ hộp" |
| BR-09 | Chẩn đoán chỉ để hiển thị ("Bệnh: …"), không dùng cho quyết định nào |
| BR-10 | Không lưu ảnh thuốc ở đâu cả; không lưu họ tên, số BHYT dạng chữ; server không lưu gì. Ảnh đơn gốc chỉ lưu trong bộ nhớ riêng của app trên điện thoại, xóa cùng đơn, chỉ rời máy khi gửi đọc đơn hoặc khi người dùng tự bấm "Gửi người thân" ([ADR-016](../architecture/adr/prescription-image-on-device.md)) |
| BR-11 | Chuẩn an toàn ≤ 2% không bao giờ nới; ngưỡng trong `deploy_config.json` không sửa tay |
| BR-12 | Mỗi lúc chỉ có một đơn đang dùng; cữ, nhắc và kiểm thuốc chỉ theo đơn đó. Đơn mới thay đơn cũ sau khi người dùng xác nhận |

## 10. Nguồn

Tổng hợp từ các tài liệu cũ (nay ở `docs/archive/`): sản phẩm và trải nghiệm (`MediCheck_brainstorm.md`), sổ quyết định kỹ thuật (`MediCheck_decisions.md` mục 0–11), phân tích dữ liệu (`vaipe_analysis.md`).
