# AGENTS.md

Hướng dẫn cho AI coding agent (Claude Code, Cursor, Copilot, Codex…) và người mới làm việc trên repo này. Đọc hết file này trước khi sửa code.

## Dự án

MediCheck VN: app Flutter giúp người cao tuổi kiểm thuốc theo đơn qua camera. Repo gồm:
- `backend/`: server AI (FastAPI, ONNX Runtime CPU) – **đã xong, đã đo an toàn**;
- `out/onnx_final/`: mô hình đã chốt;
- `mobile/`: app Flutter – **đang làm** (chưa tạo);
- `docs/`: tài liệu, bắt đầu từ [docs/README.md](docs/README.md).

## Trước khi làm một việc

Luồng plan → code → review → PR và vai trò của từng công cụ AI: [docs/process/ai-workflow.md](docs/process/ai-workflow.md). Không push thẳng `main`; mỗi story một nhánh `story/ST-xx-…` và một PR.

1. Tìm task trong [docs/product/backlog.md](docs/product/backlog.md) và trạng thái ở [docs/product/tasks.csv](docs/product/tasks.csv) (task `Todo` đầu tiên có mọi phụ thuộc `Done`); chỉ làm **một** story mỗi lần.
2. Làm màn hình nào thì mở thiết kế của màn đó: `docs/design/png/<màn>.png` và `docs/design/screens/<màn>.html` (tên file ghi ở mục "Thiết kế" của story trong backlog); token và linh kiện ở [docs/design/design-spec.md](docs/design/design-spec.md). Dựng xong phải so được với ảnh chuẩn.
3. Đọc các mã FR/UC/SCR mà story trỏ tới, cùng [docs/architecture/erd.md](docs/architecture/erd.md) và [docs/architecture/openapi.yaml](docs/architecture/openapi.yaml) nếu chạm dữ liệu hoặc API.
4. Gặp chỗ tài liệu không nói, hoặc mục `OQ-xx` chưa "Đã chốt": **hỏi người phụ trách**, không tự quyết.
5. Xong thì đổi trạng thái task trong `tasks.csv` và cập nhật tài liệu bị ảnh hưởng trong cùng commit.

## Quy tắc không được phá

- **BR-01:** app chỉ hiện cữ xanh và nút "Tôi đã uống" khi server trả `status = "green"`. Lỗi, timeout, mất mạng, JSON hỏng → không bao giờ xanh.
- Không sửa `out/onnx_final/` (`deploy_config.json`, bảng tra, file ONNX) và không đổi ngưỡng trong code.
- Không chạy đánh giá trên tập test (`--fold test`, `--unseal-test`): tập test đã dùng một lần ([ADR-008](docs/architecture/adr/safety-rule-and-sealed-test.md)).
- **BR-10 / [ADR-016](docs/architecture/adr/prescription-image-on-device.md):** không lưu ảnh thuốc; không lưu họ tên, số BHYT dạng chữ; ảnh đơn gốc chỉ ở thư mục riêng của app và xóa cùng đơn; không log nội dung đơn.
- **BR-12:** chỉ một đơn `active`; lưu đơn mới thì đơn cũ `ended` trong cùng transaction.
- Không thêm câu chữ có "an toàn", "chắc chắn đúng", "có thể là thuốc…", hay tên màu viên. Câu chữ của app chỉ nằm trong `mobile/lib/core/strings_vi.dart`.
- Gửi `name` cho `/v1/pills/verify` đúng chuỗi `matched_name` server trả, không gửi chữ OCR thô.
- Không thêm thư viện ngoài [ADR-015](docs/architecture/adr/flutter-app-stack.md) khi chưa có ADR mới.
- Không thêm AI làm tác giả hay đồng tác giả trong commit (không có dòng `Co-Authored-By` của AI).

## Lệnh

```bash
# Server bằng Docker (cách chính, ADR-017): từ thư mục gốc repo
docker compose up --build -d                                                     # tắt: docker compose down

# Server bằng Python (dự phòng / khi sửa code backend; Python 3.10–3.13)
python -m pip install -r backend/requirements.txt
python -m uvicorn backend.medicheck_server.app:app --host 0.0.0.0 --port 8000   # thử: http://localhost:8000/docs
python backend/tests/test_decide.py                                              # test logic quyết định
python -m backend.export_openapi                                                 # sinh lại docs/architecture/openapi.yaml sau khi sửa app.py

# App (khi mobile/ đã tạo)
cd mobile && flutter pub get && flutter analyze && flutter test
flutter run                                                                      # máy giả lập gọi server ở http://10.0.2.2:8000
dart run build_runner build --delete-conflicting-outputs                        # sau khi sửa bảng drift
```

## Quy ước code

- App: cấu trúc feature-first như [system-architecture.md](docs/architecture/system-architecture.md) mục 4.2; logic nghiệp vụ ở `lib/core/domain` bằng Dart thuần, kèm unit test.
- Tên trong code theo [docs/glossary.md](docs/glossary.md) (`session`, `drug_line`, `dose_event`…).
- Mọi chuỗi JSON là UTF-8 (`utf8.decode(res.bodyBytes)`).
- Mỗi màn hình theo đặc tả `SCR-xx` ở [ui-ux-spec.md](docs/product/ui-ux-spec.md) và **giống bản thiết kế** ở [docs/design/](docs/design/README.md): một nút chính, chữ ≥ 20 sp, vùng chạm ≥ 48 dp, có `Semantics` tiếng Việt. Màu, cỡ chữ, khoảng cách chỉ lấy từ token (`mobile/lib/app/tokens.dart`), không viết số rời. Khác thiết kế thì hỏi trước.

## Định nghĩa "xong"

- Tiêu chí chấp nhận của các FR liên quan đạt; ca TC liên quan trong [test-plan.md](docs/quality/test-plan.md) đạt.
- `flutter analyze` sạch, `flutter test` xanh; đổi `backend/` thì `test_decide.py` xanh và `openapi.yaml` đã sinh lại.
- Tài liệu bị ảnh hưởng đã cập nhật.

## Không đưa lên repo

Dữ liệu thô, ảnh người dùng, báo cáo `.docx`, log thí nghiệm, token (Kaggle hay bất kỳ dịch vụ nào). `.gitignore` chỉ cho phép một số đường dẫn; thêm thư mục mới (ví dụ `mobile/`) thì phải mở trong `.gitignore`.
