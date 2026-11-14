# ADR-010: OCR bằng PP-OCRv5 + VietOCR (ONNX) + luật tách trường

- **Trạng thái:** Đã chấp nhận
- **Ngày:** 2026-11-09
- **Người quyết:** phụ trách AI

## Bối cảnh

Đơn BHYT của VAIPE có 2 mẫu cố định; cần đọc tên, số lượng, lịch, ghi chú ăn, ngày kê, chẩn đoán; chạy CPU; không train lại.

## Quyết định

- PP-OCRv5 mobile det → chỉnh nghiêng, gom hàng → VietOCR `vgg_transformer` → luật tách trường → khớp mờ với 138 tên (cutoff 0,8). Cả hai mô hình xuất sang **ONNX** (khớp bản gốc 180/180 ô chữ), server không cần Paddle hay PyTorch.
- Đường chính là **chọn ảnh/PDF đơn**; chụp giấy là đường phụ.
- **Màn xác nhận bắt buộc** với mọi đơn.
- Chẩn đoán chỉ hiển thị.

## Phương án đã cân nhắc

| Phương án | Vì sao không chọn |
|---|---|
| PP-OCRv5 recognition (latin) | Lịch uống chỉ đúng 40% (mất dấu "Chiều") so với 98% của VietOCR |
| PhoBERTGrid + Swin (SOICT 2023) | Nặng, cần GPU; đơn mẫu cố định nên luật là đủ; để giai đoạn 2 |
| VLM qua API | Tốn tiền, gửi dữ liệu y tế ra ngoài, nguy cơ bịa liều |

## Hệ quả

- Test (một lần): 99,85% dòng thuốc đúng hoàn toàn trên ảnh gốc, 98,93% trên ảnh mô phỏng chụp giấy; ~5 giây/đơn.
- **Chưa đo trên ảnh chụp giấy thật**: màn xác nhận là lưới an toàn.
- Chỉ phủ 2 mẫu đơn VAIPE.
