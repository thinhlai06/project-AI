# Tài liệu cũ (lưu trữ)

Các file ở đây là tài liệu làm việc trước khi có bộ tài liệu hiện tại (14–15/11/2026). **Không cập nhật nữa.** Khi mâu thuẫn với tài liệu ngoài thư mục này, tài liệu ngoài là đúng ([../README.md](../README.md), mục "Thứ tự ưu tiên").

Giữ lại vì chứa số đo, lý do và trích dẫn mà báo cáo và buổi bảo vệ cần.

| File | Nội dung | Thay bằng |
|---|---|---|
| [MediCheck_decisions.md](MediCheck_decisions.md) | Sổ quyết định kỹ thuật: số đo từng thí nghiệm, lý do chọn mô hình, ngưỡng, kết quả test | [../architecture/adr/](../architecture/adr/README.md), [../ai/model-card.md](../ai/model-card.md) |
| [MediCheck_AI_tong_hop.md](MediCheck_AI_tong_hop.md) | Tổng hợp toàn bộ phần AI để viết báo cáo | [../ai/model-card.md](../ai/model-card.md) |
| [MediCheck_brainstorm.md](MediCheck_brainstorm.md) | Ý tưởng sản phẩm, trải nghiệm người cao tuổi | [../product/business-analysis.md](../product/business-analysis.md), [../product/prd.md](../product/prd.md) |
| [MediCheck_AI_progress.md](MediCheck_AI_progress.md) | Nhật ký tiến độ phần AI | [../product/roadmap.md](../product/roadmap.md) |
| [MediCheck_citation_evidence.md](MediCheck_citation_evidence.md) | Nguồn trích dẫn cho báo cáo | – |
| [vaipe_analysis.md](vaipe_analysis.md) | Phân tích dữ liệu VAIPE | [../ai/dataset.md](../ai/dataset.md) |

## Chỗ đã lỗi thời

- `MediCheck_decisions.md` mục 8: OCR chạy bằng PyTorch/Paddle và Python 3.10. Nay OCR chạy bằng ONNX trong server, Python 3.10–3.13 ([ADR-010](../architecture/adr/ocr-onnx-rule-parser.md)).
- Mọi chỗ nói "không lưu ảnh đơn": nay ảnh đơn gốc được lưu trong app để gửi người thân ([ADR-016](../architecture/adr/prescription-image-on-device.md)).
- Mọi chỗ nói nhiều đơn cùng hiệu lực: nay chỉ một đơn đang dùng (BR-12).
- Đường dẫn trong các file là đường dẫn lúc file còn ở thư mục gốc repo.
