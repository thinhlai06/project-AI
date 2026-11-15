# Quy trình làm việc với AI: Claude lên plan và review, Qoder viết code

> **Trả lời câu hỏi:** một story đi từ backlog tới main như thế nào khi dùng Claude Code và Qoder CLI.
> Luật code chung cho mọi agent ở [../../AGENTS.md](../../AGENTS.md); file này chỉ nói về **luồng** và **vai trò**.
> Cập nhật: 2026-11-15 · Trạng thái: **đã chốt**

## 1. Vai trò

| Ai | Làm | Không làm |
|---|---|---|
| **Chủ dự án** (người giao việc) | Chọn story, duyệt plan, trả lời câu hỏi, **merge PR** | – |
| **Claude Code** | Đọc docs, lập plan, gọi Qoder theo từng phase, kiểm diff, chạy test, commit, push, tạo PR, review PR | Tự viết code tính năng (trừ sửa một dòng hiển nhiên khi Qoder đã thử 3 lần); merge PR; sửa docs khi chưa hỏi |
| **Qoder CLI** | Sửa đúng các file được giao trong một phase, chạy `flutter analyze` / `flutter test` để tự kiểm | Mọi lệnh git ghi, `gh`, sửa file ngoài danh sách, thêm thư viện |

Chỉ Claude (hoặc người) giữ quyền ghi git, để không lọt commit sai nhánh, file cấm hay dòng tác giả AI.

## 2. Luồng một story

```mermaid
flowchart LR
  A[Chọn story ST-xx] --> B[Claude: plan]
  B --> C{Chủ dự án duyệt?}
  C -- sửa --> B
  C -- duyệt --> D[Tạo nhánh]
  D --> E[Qoder: phase N]
  E --> F[Claude: kiểm diff + test]
  F -- lỗi, ≤ 3 vòng --> E
  F -- đạt --> G[Commit + push]
  G -- còn phase --> E
  G -- hết phase --> H[Claude: self-review + tạo PR]
  H --> I[Claude: review PR, sửa qua Qoder]
  I --> J[Chủ dự án merge]
```

1. **Chọn story:** story chứa task `Todo` có `Thứ tự làm` nhỏ nhất trong [../product/tasks.csv](../product/tasks.csv) (mô tả task ở [../product/backlog.md](../product/backlog.md)). Mỗi task là một phase giao cho Qoder.
2. **Plan:** Claude đọc các FR/UC/SCR/TC mà story trỏ tới, cùng erd/openapi nếu chạm dữ liệu hoặc API, rồi viết `.ai-work/ST-xx/PLAN.md` (local, không commit):
   - mục tiêu và tiêu chí chấp nhận, chép nguyên từ PRD;
   - chia **phase** nhỏ, mỗi phase: file được sửa, việc làm, test phải có, lệnh kiểm;
   - rủi ro, chỗ chạm BR-01 / BR-10 / BR-12;
   - câu hỏi kèm đề xuất. Chỗ docs không nói → ghi `OQ-xx` mới vào PRD sau khi chủ dự án trả lời.
3. **Duyệt plan:** chỉ làm tiếp khi chủ dự án nói "duyệt".
4. **Nhánh:** `git switch -c story/ST-xx-<mo-ta-ngan> origin/main`, rồi `git push -u origin HEAD`.
5. **Từng phase:** Claude gọi Qoder (mục 3) → kiểm (mục 4) → đạt thì commit đúng file và push.
6. **Self-review:** Claude đọc `git diff origin/main...HEAD` thật, rà theo checklist mục 5, sửa qua Qoder.
7. **PR:** `gh pr create --base main --title "<type>(ST-xx): ..." --body-file .ai-work/ST-xx/PR_BODY.md`. Body gồm: story, FR/SCR/TC liên quan, đã làm gì, docs đổi gì, cách test, ảnh chụp màn hình emulator, giới hạn.
8. **Review PR:** Claude review lại bản trên GitHub và post bằng `gh pr review <n> --comment`. Còn lỗi → Qoder sửa → commit → review lại, tối đa 3 vòng.
9. **Merge:** chủ dự án merge (squash) trên GitHub. Claude đổi trạng thái các task của story thành `Done` trong `tasks.csv` (trong chính PR của story; khi chạy song song thì làm ở commit riêng sau merge, mục 2b), rồi xóa nhánh local.

## 2b. Làm nhiều story song song bằng worktree (tùy chọn)

**Mặc định làm tuần tự** (mục 2). Chỉ dùng worktree khi hai story **độc lập** và bạn muốn Qoder chạy cùng lúc. Phần lớn đường chính là chuỗi phụ thuộc (ST-06 → 07 → 09; ST-11, 12 → 13 → 14, 15), nên song song ít khi có lợi.

**Cặp có thể chạy song song** (khác thư mục, khác phụ thuộc):
- ST-08 (logic Dart thuần) ∥ ST-04 (client API) ∥ ST-03 (database) ∥ ST-02.
- ST-10 (nhắc thuốc) ∥ ST-12 (camera, chuẩn bị ảnh) ∥ ST-11.1 (giọng nói).
- ST-17, ST-18, ST-19, ST-21 với nhau (sau khi ST-15 xong).
- ST-05 (đo tốc độ), ST-27 (giấy phép), ST-28 (CI) với bất kỳ story nào (không đụng `mobile/`).

**Luật:**
1. Tối đa **2 worktree** cùng lúc; mỗi worktree một story một nhánh `story/ST-xx-…`; không dùng chung. Không sửa code ở thư mục chính khi đang có worktree.
2. Tạo worktree **ngoài** repo, từ `main` mới nhất:
   ```powershell
   git fetch origin
   git worktree add -b story/ST-xx-<mo-ta> "d:\project AI_wt\ST-xx" origin/main
   cd "d:\project AI_wt\ST-xx\mobile"; flutter pub get
   ```
   Gọi Qoder với `-w "d:\project AI_wt\ST-xx"`. Plan và nhật ký vẫn ở `d:\project AI\.ai-work\ST-xx\` (dùng đường dẫn tuyệt đối).
3. **Máy giả lập chỉ chạy một bản app** (cùng `applicationId`): chạy thử story nào thì cài từ worktree đó; chuyển story thì gỡ rồi cài lại. Server Docker dùng chung được (không có trạng thái).
4. **Chỗ dễ xung đột** khi hai nhánh cùng sửa: `strings_vi.dart`, `app/router.dart`, `app/providers.dart`, file drift sinh ra. Mỗi story chỉ **thêm** vào cuối các file này (khối riêng theo story), không sắp xếp lại. Gặp xung đột thì giải trong file của story mình; nếu ở file khác thì dừng, hỏi chủ dự án.
5. **Không đổi `tasks.csv` trong PR story** khi chạy song song (xung đột chắc chắn). Sau khi chủ dự án merge, Claude đổi trạng thái trên `main` bằng một commit riêng `chore: mark ST-xx done`.
6. **Đồng bộ:** story merge trước thì story còn lại `git rebase origin/main`, chạy `dart run build_runner build --delete-conflicting-outputs` nếu đụng drift, `flutter analyze` và `flutter test` lại, rồi `push --force-with-lease` (chỉ nhánh của mình). **Không rebase khi Qoder đang chạy ở worktree đó.**
7. Dọn sau khi merge: `git worktree remove "d:\project AI_wt\ST-xx"`, `git worktree prune`, `git branch -d story/ST-xx-…` (chỉ `-d`). Không dùng `--force` khi còn thay đổi chưa commit.
8. Trước mỗi lệnh git ghi: `git rev-parse --show-toplevel` và `git branch --show-current` phải khớp story đang làm.

## 3. Gọi Qoder

Giao một phase (task có màn hình thì thêm vào lời giao: `UI reference: docs/design/png/<màn>.png and docs/design/screens/<màn>.html; tokens in docs/design/design-spec.md. Match them; do not invent colors, sizes or text.`):

```powershell
qodercli -p -w "d:\project AI" -n "ST-xx-p<N>" --permission-mode accept_edits `
  --append-system-prompt "You implement code for MediCheck. Follow AGENTS.md strictly. NEVER run git write commands, never call gh, never run 'qodercli commit'. Edit ONLY the files listed. Do not add packages or edit pubspec.yaml, AndroidManifest.xml, Info.plist, docs/ or backend/ unless explicitly allowed below. All user-facing text goes in mobile/lib/core/strings_vi.dart. Never add AI attribution." `
  "Implement ONLY Phase <N> of d:\project AI\.ai-work\ST-xx\PLAN.md.
   Allowed files: <list>. Explicitly allowed extras: <none | ...>.
   Exit criteria: <from plan>.
   Then run in mobile/: flutter analyze; flutter test.
   Report: files changed, commands run with results, anything not done and why."
```

Giao sửa lỗi (giữ ngữ cảnh phiên cũ):

```powershell
qodercli -p -w "d:\project AI" -r <session-id> --permission-mode accept_edits `
  "Fix ONLY: 1) <file:line> – <problem> – <expected fix> (rule <BR/FR/TC>). Then run flutter analyze; flutter test and report."
```

Ghi chú vận hành (lần đầu dùng, kết quả thực tế, lỗi gặp) vào `.ai-work/NOTES.md`.

## 4. Claude kiểm sau mỗi lần Qoder chạy

```bash
git status --short          # chỉ có file trong danh sách cho phép
git diff --stat
git log -1 --oneline        # không có commit lạ
cd mobile && flutter analyze && flutter test
```

- File ngoài danh sách bị sửa → `git restore <file>`, báo Qoder.
- Có commit hoặc nhánh lạ → dừng, báo chủ dự án.
- Test mới phải **fail trước khi sửa và pass sau khi sửa** (với logic ở `core/domain`).
- Story có màn hình → chạy trên emulator, chụp màn hình vào `.ai-work/ST-xx/evidence/`. Tắt server và emulator khi xong.

## 5. Checklist review (mỗi PR)

- [ ] Đạt tiêu chí chấp nhận của từng FR; TC liên quan đạt.
- [ ] **BR-01:** không có đường nào hiện xanh hay "Tôi đã uống" khi `status != "green"`, kể cả lỗi/timeout.
- [ ] **BR-10 / ADR-016:** không lưu ảnh thuốc; ảnh đơn chỉ ở thư mục app; không log nội dung đơn.
- [ ] **BR-12:** không tạo được 2 đơn `active`.
- [ ] Giao diện khớp ảnh chuẩn `docs/design/png/` (so ảnh chụp emulator 390 × 844); dùng token, không số rời.
- [ ] Chữ hiển thị chỉ ở `strings_vi.dart`, không có từ cấm; chữ ≥ 20 sp, vùng chạm ≥ 48 dp, có `Semantics`.
- [ ] DTO khớp `openapi.yaml`; `utf8.decode(res.bodyBytes)`.
- [ ] Không thêm thư viện ngoài ADR-015; không sửa `out/onnx_final/`.
- [ ] Docs bị ảnh hưởng đã sửa trong cùng PR.

## 6. Git

- Nhánh: `story/ST-xx-<mo-ta>`, sửa lỗi `fix/<mo-ta>`, tài liệu `docs/<mo-ta>`. Một nhánh một story.
- Commit: `<type>(ST-xx): <tóm tắt>`; `type` ∈ `feat|fix|refactor|test|docs|chore`; tiếng Anh, mệnh lệnh, ≤ 20 từ. Một commit một thay đổi logic.
- Chỉ `git add <đường dẫn cụ thể>`; không `git add -A`, `git add .`, `git commit -a`.
- Không push thẳng `main`; không force-push `main`; `--force-with-lease` chỉ trên nhánh của chính mình.
- Không có dòng `Co-Authored-By` hay "Generated with" của AI trong commit, PR, review.
- Không commit `.ai-work/`, ảnh bằng chứng, `*.db`, token, `build/`, `.dart_tool/`.

## 7. Dừng và hỏi chủ dự án khi

- Một lỗi sửa quá 3 vòng, hoặc review PR quá 3 vòng chưa đạt.
- Cần sửa docs, thêm thư viện, đổi `pubspec.yaml` ngoài plan, đổi API server.
- Docs mâu thuẫn nhau, hoặc gặp `OQ-xx` chưa chốt.
- Qoder sửa ngoài phạm vi hay chạy lệnh git.
