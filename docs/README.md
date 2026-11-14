# Tài liệu MediCheck

Mục lục bộ tài liệu. Mỗi file trả lời **một** câu hỏi; khi hai file mâu thuẫn, file đứng trên trong bảng "Thứ tự ưu tiên" là đúng, và file sai phải được sửa ngay.

## Bản đồ

| Câu hỏi | File |
|---|---|
| Vì sao làm, cho ai, giới hạn gì, quy tắc nghiệp vụ (BR-xx) | [product/business-analysis.md](product/business-analysis.md) |
| App phải làm gì, đến mức nào là xong (FR-xx, NFR-xx, OQ-xx) | [product/prd.md](product/prd.md) |
| Ai làm gì theo trình tự nào (UC-xx) | [product/use-cases.md](product/use-cases.md) |
| Từng màn hình trông và nói thế nào (SCR-xx, MSG-xx) | [product/ui-ux-spec.md](product/ui-ux-spec.md) |
| Làm gì trước, làm gì sau (M-x, ST-xx) | [product/roadmap.md](product/roadmap.md) |
| Hệ thống gồm những phần nào, code app tổ chức ra sao | [architecture/system-architecture.md](architecture/system-architecture.md) |
| Database trên điện thoại | [architecture/erd.md](architecture/erd.md) |
| Hợp đồng API (máy đọc được, sinh từ code) | [architecture/openapi.yaml](architecture/openapi.yaml) |
| Hướng dẫn API có ví dụ JSON, curl, Dart | [../backend/API.md](../backend/API.md) |
| Chạy server và demo trên laptop | [architecture/deployment.md](architecture/deployment.md) |
| Vì sao chọn như vậy (ADR-xxx) | [architecture/adr/README.md](architecture/adr/README.md) |
| Mô hình AI: làm được gì, giỏi đến đâu, giới hạn | [ai/model-card.md](ai/model-card.md) |
| Dữ liệu huấn luyện và cách tạo lại | [ai/dataset.md](ai/dataset.md) |
| Kiểm cái gì, khi nào là đạt (TC-xx) | [quality/test-plan.md](quality/test-plan.md) |
| Làm việc với AI (Claude plan/review, Qoder code), nhánh, PR | [process/ai-workflow.md](process/ai-workflow.md) |
| Nghĩa của từng từ | [glossary.md](glossary.md) |
| Sơ đồ pipeline (PNG + nguồn Mermaid) | [diagrams/](diagrams/) |
| Tài liệu cũ (tham khảo, không cập nhật nữa) | [archive/](archive/) |

## Thứ tự ưu tiên khi mâu thuẫn

1. ADR có trạng thái "Đã chấp nhận".
2. `business-analysis.md` (quy tắc BR-xx).
3. `prd.md`.
4. `openapi.yaml` (cho hình dạng API) và `erd.md` (cho dữ liệu).
5. `use-cases.md`, `ui-ux-spec.md`, `system-architecture.md`.
6. Mọi thứ trong `archive/`.

## Thứ tự đọc

| Vai trò | Đọc |
|---|---|
| AI agent viết code | [../AGENTS.md](../AGENTS.md) → [process/ai-workflow.md](process/ai-workflow.md) → roadmap (story đang làm) → các FR/UC/SCR mà story trỏ tới → erd / openapi |
| Lập trình viên mobile mới | business-analysis → prd → ui-ux-spec → system-architecture → erd → backend/API.md |
| Người chạy demo | deployment → test-plan mục 5 |
| Người chuẩn bị bảo vệ | model-card → dataset → ADR-005 … ADR-010 → `archive/MediCheck_AI_tong_hop.md` |

## Quy ước

- **Mã định danh:** `BR-` quy tắc nghiệp vụ, `FR-`/`NFR-` yêu cầu, `OQ-` câu hỏi mở, `UC-` use case, `SCR-` màn hình, `MSG-` câu chữ, `ST-` story, `TC-` ca kiểm thử, `ADR-` quyết định. Mã không bao giờ dùng lại; xóa thì ghi "(bỏ)".
- **Tên file:** kebab-case tiếng Anh, không đánh số. Nội dung tiếng Việt; tên trong code, API, database bằng tiếng Anh như [glossary.md](glossary.md).
- **Đầu mỗi file:** câu hỏi file trả lời, ngày cập nhật, trạng thái (`nháp chờ duyệt` / `đã chốt`).
- **Đổi quyết định:** viết ADR mới trước, rồi sửa các file bị ảnh hưởng trong cùng commit.
- **Đổi API:** sửa `backend/medicheck_server/app.py`, chạy `python -m backend.export_openapi`, cập nhật `backend/API.md` nếu cần.
- **Sơ đồ:** sửa file `.mmd` rồi render lại PNG: `npx -p @mermaid-js/mermaid-cli@11.4.2 mmdc -i x.mmd -o x.png -s 2 -b white`.
