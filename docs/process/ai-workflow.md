# Quy trình làm việc với AI: Claude lên plan và review, Qoder viết code

> **Trả lời câu hỏi:** một story đi từ backlog tới main như thế nào khi dùng Claude Code và Qoder CLI.
> Luật code chung cho mọi agent ở [../../AGENTS.md](../../AGENTS.md); file này chỉ nói về **luồng** và **vai trò**.
> Nhật ký vận hành (lỗi gặp, cách xử lý, đề xuất cải tiến luồng): [workflow-log.md](workflow-log.md). Mục 8 nói cách ghi.
> Cập nhật: 2026-11-16 · Trạng thái: **đã chốt**

## 1. Vai trò

| Ai | Làm | Không làm |
|---|---|---|
| **Chủ dự án** (người giao việc) | Chọn story, duyệt plan, trả lời câu hỏi, **merge PR** (hoặc cho phép Claude merge cho đúng PR đó, mục 5b) | – |
| **Claude Code** | Đọc docs, lập plan, gọi Qoder theo từng phase, kiểm diff, chạy test, commit, push, tạo PR, review PR, **ghi nhật ký vận hành** (mục 8) | Tự viết code tính năng (trừ sửa một dòng hiển nhiên khi Qoder đã thử 3 lần); merge PR (trừ khi cổng merge mục 5b đã đạt **và** chủ dự án cho phép bằng lời cho đúng PR đó); sửa docs khi chưa hỏi (trừ `tasks.csv` ở bước 6 hoặc 2b.3-8, `workflow-log.md` ở mục 8 và `docs/process/machine-installs.md` khi story cài thứ gì ngoài repo) |
| **Qoder CLI** | Sửa đúng các file được giao trong một phase **và chạy các lệnh trong danh sách cho phép của phase đó** (`flutter create/pub/analyze/test/build`, mục 3b), tự kiểm và báo kết quả | Mọi lệnh git ghi, `gh`, sửa file ngoài danh sách, thêm thư viện ngoài ADR-015 (hoặc ngoài danh sách trong task file) |

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
  I --> J[Cổng merge mục 5b rồi merge]
```

1. **Chọn story:** story chứa task `Todo` có `Thứ tự làm` nhỏ nhất trong [../product/tasks.csv](../product/tasks.csv) (mô tả task ở [../product/backlog.md](../product/backlog.md)). Mỗi task là một phase giao cho Qoder.
2. **Plan:** Claude đọc các FR/UC/SCR/TC mà story trỏ tới, cùng erd/openapi nếu chạm dữ liệu hoặc API, rồi viết `.ai-work/ST-xx/PLAN.md` (local, không commit):
   - mục tiêu và tiêu chí chấp nhận, chép nguyên từ PRD;
   - chia **phase** nhỏ, mỗi phase: file được sửa, việc làm, test phải có, lệnh kiểm;
   - rủi ro, chỗ chạm BR-01 / BR-10 / BR-12;
   - câu hỏi kèm đề xuất. Chỗ docs không nói → ghi `OQ-xx` mới vào PRD sau khi chủ dự án trả lời.
3. **Duyệt plan:** chỉ làm tiếp khi chủ dự án nói "duyệt".
4. **Nhánh:** `git fetch origin`, rồi `git switch -c story/ST-xx-<mo-ta-ngan> origin/main`, rồi `git push -u origin HEAD`. Luồng một story làm ở thư mục chính; 2b.1 (worktree) chỉ áp dụng khi mở nhiều story cùng lúc.
5. **Từng phase:** Claude gọi Qoder (mục 3) → kiểm (mục 4) → đạt thì commit đúng file và push. Có trục trặc thì ghi ngay vào nhật ký (mục 8).
6. **Self-review:** Claude đọc `git diff origin/main...HEAD` thật (với nhánh xếp chồng: `<nhánh-cha>...HEAD`), rà theo checklist mục 5, sửa qua Qoder. Sau self-review đạt, trước khi tạo PR: một commit riêng `chore(ST-xx): mark done` đổi trạng thái các task của story trong `tasks.csv` và, nếu có gì đáng ghi, thêm 1–3 dòng nhìn lại vào `workflow-log.md` (mục 8.3 bước 5), để hai thay đổi này được review cùng PR. Khi chạy song song (có từ 2 story mở cùng lúc, mục 2b) thì bỏ commit này và làm sau merge (bước 9, 2b.3-8).
7. **PR:** `gh pr create --base main --title "<type>(ST-xx): ..." --body-file "d:/project AI/.ai-work/ST-xx/PR_BODY.md"`. Body gồm: story, FR/SCR/TC liên quan, đã làm gì, docs đổi gì, cách test, mô tả và đường dẫn ảnh chụp emulator ở `.ai-work/ST-xx/evidence/` (ảnh không commit; chủ dự án tự đính nếu cần), giới hạn.
8. **Review PR (bắt buộc, theo mục 5b):** Claude review bản diff thật trên GitHub bằng prompt chuẩn ở mục 5b (có thể chạy song song subagent theo từng trục) và post mỗi vòng bằng `gh pr review <n> --comment`. Còn High/Medium → Qoder sửa → commit → review lại toàn bộ diff mới, tối đa 3 vòng; vòng 3 chưa đạt thì dừng và hỏi chủ dự án (mục 7). **3 là trần, không phải số vòng bắt buộc:** PR đạt cổng merge (mục 5b) ở vòng nào, kể cả vòng 1, thì được merge ngay ở vòng đó, không cần review thêm cho đủ 3 vòng.
9. **Merge:** Claude chỉ merge khi PR đã đạt **cổng merge ở mục 5b** và chủ dự án cho phép bằng lời cho đúng PR đó (lệnh merge: `gh pr merge <n> --squash`); không thì chủ dự án merge (squash) trên GitHub (chủ dự án tự merge trên GitHub là quyền của họ, ngoài luồng này). Cổng chưa đạt thì Claude không merge. Trạng thái `Done` đã đổi ở bước 6 (hoặc làm sau merge nếu chạy song song, mục 2b.3-8). Dọn sau merge theo đúng thứ tự: (a) `gh pr view <n> --json state,headRefName,headRefOid` ra state MERGED; (b) nếu story có worktree: `git -C <worktree> status --short` rỗng, rồi `git worktree remove <worktree>` (không `--force`); (c) `git switch main`, `git pull`; (d) `git branch -D <headRefName>` (squash merge làm `git branch -d` báo 'not fully merged', nên đây là ngoại lệ của 2b.3-4) chỉ khi state = MERGED, `git status` sạch, tên nhánh đúng bằng headRefName của PR và khác `main`, và `git rev-parse <nhánh>` bằng headRefOid (không mất commit chưa push); (e) `git push origin --delete <headRefName>` chỉ sau khi (d) thành công; (f) `git worktree prune`. Không xóa nhánh cha khi nhánh con xếp chồng chưa `rebase --onto` (2b.4).

## 2b. Làm 2–3 story cùng lúc (worktree + nhánh xếp chồng)

Bạn vẫn làm **tuần tự theo phụ thuộc**, nhưng mở 2–3 story cùng lúc để Qoder không phải chờ. Hai loại quan hệ (xem cột `Phụ thuộc` trong [../product/tasks.csv](../product/tasks.csv)):

| Quan hệ | Gốc của nhánh mới | PR |
|---|---|---|
| **Độc lập** (không phụ thuộc story nào đang mở) | `origin/main` mới nhất | PR thường |
| **Phụ thuộc story cha của chính bạn chưa merge** | **nhánh của story cha** (xếp chồng) | PR **Draft** cho tới khi cha merge (mục 2b.5) |

Chỉ xếp chồng lên nhánh **của chính mình**. Chuỗi gợi ý: ST-06 ← ST-07 ← ST-09 (sâu 3); ST-11 ← ST-13 ← ST-14. Cặp độc lập: ST-02 ∥ ST-03 ∥ ST-04 ∥ ST-08; ST-10 ∥ ST-12; ST-17 ∥ ST-18 ∥ ST-19 ∥ ST-21; ST-05, ST-27, ST-28 với bất kỳ story nào (không đụng `mobile/`).

### 2b.1 Bố cục

```
d:\project AI\                       ← thư mục chính: chỉ fetch, quản lý worktree, đứng ở main; KHÔNG sửa code ở đây
d:\project AI_wt\ST-xx\              ← worktree của story ST-xx (nhánh story/ST-xx-…)
d:\project AI\.ai-work\ST-xx\        ← plan, log, bằng chứng (đường dẫn tuyệt đối; không commit)
d:\project AI\.ai-work\STACKS.md     ← quan hệ xếp chồng và việc "cần rebase sau phase này"
```

### 2b.2 Tạo

```powershell
cd "d:\project AI"
git fetch origin --prune
# Độc lập: gốc là main
git worktree add -b story/ST-06-import "d:\project AI_wt\ST-06" origin/main
# Xếp chồng: gốc là nhánh cha (của chính bạn, chưa merge)
git worktree add -b story/ST-07-confirm "d:\project AI_wt\ST-07" story/ST-06-import
git worktree list
cd "d:\project AI_wt\ST-07\mobile"; flutter pub get      # mỗi worktree một lần
```

Trong worktree vừa tạo, đẩy nhánh bằng `git push -u origin HEAD` (không `git push` trần: nhánh đang theo dõi `origin/main`).

Ghi quan hệ vào `.ai-work/STACKS.md` (ví dụ `ST-07 ← ST-06`). Gọi Qoder với `-w "d:\project AI_wt\ST-xx"`.

### 2b.3 Luật worktree

1. **1 worktree = 1 nhánh = 1 story.** Không làm hai story trong một worktree; không sửa code ở thư mục chính.
2. Tối đa **3 worktree** mở cùng lúc; xếp chồng sâu tối đa **3** (`main` ← A ← B ← C). Worktree chỉ để review (`review-pr<N>`) hoặc chỉ để làm PR docs `docs/mark-ST-xx-done` (`d:/project AI_wt/docs-mark-ST-xx`) nằm ngoài giới hạn và phải dọn ngay sau khi xong.
3. Mọi lệnh (Qoder `-w`, `flutter`, git) chạy **trong worktree của story đó**. Trước mỗi lệnh git ghi: `git rev-parse --show-toplevel` và `git branch --show-current` phải khớp story.
4. **Không xóa worktree còn thay đổi chưa commit** (`git -C <wt> status --short` phải rỗng). Không dùng `git worktree remove --force`, không `git branch -D`, trừ khi chủ dự án đồng ý, trừ ngoại lệ ở mục 2 bước 9 (nhánh story đã squash-merge, state MERGED).
5. **Flutter:** mỗi worktree có `build/` và `.dart_tool/` riêng (không copy giữa các worktree, không commit); `PUB_CACHE` và `GRADLE_USER_HOME` dùng chung nên `pub get` nhanh. **Tại một thời điểm chỉ chạy một `flutter build apk`/`flutter run`** (Gradle tranh tài nguyên và khóa nhau); `flutter analyze` và `flutter test` thì chạy song song được.
6. **Máy giả lập chỉ chạy một bản app** (cùng `applicationId`): chạy thử story nào thì cài từ worktree đó, chuyển story thì gỡ rồi cài lại. **Server Docker dùng chung** được (không có trạng thái).
7. **Chỗ dễ xung đột:** `strings_vi.dart`, `app/router.dart`, `app/providers.dart`, file drift sinh ra, `pubspec.lock`. Mỗi story chỉ **thêm khối riêng ở cuối** các file này, không sắp xếp lại, không đổi thứ tự. Thêm thư viện cần ADR mới nên không xảy ra ở giai đoạn code.
8. **`tasks.csv` không đổi trong PR story.** Sau khi PR được merge, Claude đổi trạng thái bằng một PR docs nhỏ riêng (nhánh `docs/mark-ST-xx-done`, commit `chore(ST-xx): mark done`), không push thẳng `main` (mục 6); PR nhỏ này cũng qua mục 5b; làm ở worktree tạm `d:/project AI_wt/docs-mark-ST-xx` (mục 2b.3-2), không làm ở thư mục chính.
9. **`.gitignore` kiểu danh sách cho phép** (`/*` chặn mọi thứ): thư mục hay file mới ở gốc (ví dụ `mobile/`) **bị bỏ qua im lặng** cho tới khi được mở khóa. Trước khi `git add` đường dẫn mới: `git check-ignore -v <đường dẫn>`. Mở khóa bằng commit riêng; nếu `git add` báo "paths are ignored" thì cả lệnh add bị hủy, nên luôn đọc `git diff --cached --name-only` trước khi commit.

### 2b.4 Đồng bộ nhánh xếp chồng

- **Cha có commit mới (chưa merge)** → ở worktree con: `git rebase <nhánh-cha>`, `flutter analyze` và `flutter test` lại, `git push --force-with-lease` (chỉ khi con đã push).
- **Cha đã merge vào `main`** (squash merge nên lịch sử khác): ở worktree con
  ```powershell
  git fetch origin
  git rebase --onto origin/main <nhánh-cha> <nhánh-con>
  ```
  rồi chạy `dart run build_runner build --delete-conflicting-outputs` nếu đụng drift, `flutter analyze`, `flutter test`, `push --force-with-lease`, cập nhật `STACKS.md`.
- Luôn đồng bộ **từ dưới lên** (cha trước, con sau). Conflict chỉ giải trong file của story con; conflict ở file khác → dừng, hỏi chủ dự án. Không rebase cha theo con; không cherry-pick qua lại giữa hai story.
- **Không rebase khi Qoder (hoặc `flutter`/emulator) đang chạy ở worktree đó**: rebase đổi file dưới chân Qoder và làm phase dở hỏng. Khi cha merge mà Qoder đang chạy ở con: (1) làm ngay việc không đụng worktree con (kiểm PR đã merge, đổi trạng thái task, dọn worktree cha nếu sạch); (2) ghi "cần rebase sau phase này" vào `STACKS.md`; (3) chờ Qoder xong phase → Claude kiểm → commit → `git status --short` rỗng → **mới** rebase; (4) còn thay đổi chưa commit mà cần rebase gấp thì hỏi chủ dự án, không `stash`/`reset` để lách.

### 2b.5 PR với nhánh xếp chồng

- Mỗi story một PR, base `main`.
- Con xếp chồng mà **cha chưa merge**: PR vào `main` sẽ chứa cả commit của cha. Mở dạng **Draft** (`gh pr create --draft`), dòng đầu mô tả `Stacked on #<PR cha> – review only commits after <sha cuối của cha>`; chưa chạy review PR. Cha merge → `rebase --onto` (2b.4) → bỏ dòng stacked → `gh pr ready` → review PR (mục 2 bước 8).
- **Thứ tự merge:** cha trước, con sau. Chủ dự án không merge con trước cha.

### 2b.6 `STACKS.md` (mẫu)

```
ST-07 <- ST-06    (nhánh con story/ST-07-confirm, cha story/ST-06-import)   cần rebase sau phase này: không
ST-09 <- ST-07    cần rebase sau phase này: có (ST-06 vừa merge)
```

### 2b.7 Dùng subagent để chạy Qoder hoặc review song song

Dùng khi bạn yêu cầu hoặc có ≥ 2 việc độc lập (mỗi việc một worktree, không chung file). Prompt cho subagent ghi: worktree duy nhất được làm (subagent review chỉ đọc theo mục 5b thì không cần worktree và không cần `-n`); **không** lệnh git ghi, không lệnh `gh` ghi (đọc bằng `gh pr diff`, `gh pr view`, `gh pr checks` thì được); `-n` session mới, cấm `-c` (mục 3); danh sách file được sửa; việc cần báo cáo. **Claude không tin báo cáo của subagent**: tự đọc diff thật, tự chạy `flutter analyze` và `flutter test`, rồi mới commit và push. Việc đã commit xong mà subagent còn gửi lại báo cáo cũ khi "chờ tác vụ nền" thì dừng nó (`TaskStop`).

## 3. Gọi Qoder

Giao một phase (task có màn hình thì thêm vào lời giao: `UI reference: docs/design/png/<màn>.png and docs/design/screens/<màn>.html; tokens in docs/design/design-spec.md. Match them; do not invent colors, sizes or text.`):

```powershell
qodercli -p -w "d:\project AI" -n "ST-xx-p<N>" --permission-mode accept_edits `
  --append-system-prompt "You implement code for MediCheck. Follow AGENTS.md strictly. NEVER run git write commands, never call gh, never run 'qodercli commit'. Edit ONLY the files listed. Do not add packages or edit pubspec.yaml, AndroidManifest.xml, Info.plist, docs/ or backend/ unless explicitly allowed below, or unless the task file names the exact packages (ADR-015 only) or the exact pubspec.yaml change. All user-facing text goes in mobile/lib/core/strings_vi.dart. Never add AI attribution." `
  "Implement ONLY Phase <N> of d:\project AI\.ai-work\ST-xx\PLAN.md.
   Allowed files: <list>. Explicitly allowed extras: <none | ...>.
   Exit criteria: <from plan>.
   Try in mobile/: flutter analyze; flutter test. If you cannot run flutter here, re-read your changes for compile errors (imports, names, signatures) and say so; the orchestrator will analyze and test.
   You cannot delete or rename files: blank the old file and say so, the orchestrator removes it.
   Never use qodercli -c; you are in your own session. The orchestrator handles all git.
   If you edit a file containing Windows paths, never type a backslash before r, n, t, a, f or b (tool text mangling); prefer forward slashes and re-check the saved bytes.
   Report: files changed (full paths), commands run with results, anything not done and why."
```

Mẫu này dùng cho phase chỉ sửa file; phase có chạy lệnh `flutter` dùng mẫu ở mục 3b (có `--allowed-tools`).

Giao sửa lỗi (giữ ngữ cảnh phiên cũ):

```powershell
qodercli -p -w "d:\project AI" -r <session-id> --permission-mode accept_edits `
  "Fix ONLY: 1) <file:line> – <problem> – <expected fix> (rule <BR/FR/TC>). Raw output if from a failure: <paste verbatim>. Re-read your changes for compile errors, then report files changed."
```

**Luật khi gọi Qoder:**
- **Cấm `qodercli -c` / `--continue`**: nó nối vào session gần nhất của *bất kỳ* worktree (ở một dự án trước đã gây nhầm chéo task). Mỗi phase dùng `-n "ST-xx-p<N>"` mới; muốn tiếp tục thì chỉ `-r <session-id>` của đúng session đó ở đúng worktree đó.
- **Đã đo 2026-11-15:** `flutter` chạy được khi giao kèm danh sách cho phép hẹp (mục 3b); không cần nâng quyền (`auto`, `bypass_permissions` vẫn cấm). Claude vẫn kiểm lại bằng lệnh ngắn (chỉ lấy vài dòng cuối) và không tin câu "build OK" của Qoder.
- Qoder không xóa hay đổi tên được file (cổng quyền): nó làm rỗng file cũ; Claude chạy `git rm -f <file>` sau khi đọc diff rồi mới commit.
- **Chuỗi có dấu gạch chéo ngược đứng trước `r`, `n`, `t`** (đường dẫn Windows kiểu "backend, gạch chéo ngược, requirements.txt") có thể bị biến thành ký tự xuống dòng khi đi qua công cụ; đã làm vỡ một dòng lệnh trong `deployment.md` (nhật ký 2026-11-15). Sau khi sửa file có chuỗi như vậy, kiểm ở mức byte (python: `chr(92)` là dấu gạch chéo ngược, `bytes([13])` là CR) và đừng tin chữ hiển thị. Prompt giao Qoder cho file có đường dẫn Windows phải nhắc điều này. Trong lệnh và tài liệu mới, ưu tiên viết đường dẫn bằng dấu `/`.
- Lỗi cú pháp thường gặp của model viết code: nhầm dấu, thiếu `return`, thiếu import, gọi API Flutter không có ở bản 3.50. Gửi lỗi nguyên văn cho Qoder, một vòng thường đủ; khi một kiểu lỗi lặp lại thì thêm câu nhắc vào prompt mẫu và ghi vào nhật ký.

### 3b. Qoder làm được gì và cách giao (đo 2026-11-15)

Qoder làm được gì ở chế độ `accept_edits`:

| Việc | Mặc định | Với `--allowed-tools` hẹp |
|---|---|---|
| Sửa/tạo file trong thư mục làm việc (`-w`) | được | được |
| Đọc ngoài thư mục `-w` (ví dụ `.ai-work/`) | bị chặn | được, nếu thêm `--add-dir "<thư mục>"` |
| `git status`, `git log`, `git diff` (chỉ đọc) | được | được |
| `git add`, `git commit`, `git switch`, `gh` | bị chặn | **không cho phép** (chỉ Claude) |
| `flutter`, `dart` | bị chặn | được, đúng lệnh con đã liệt kê; riêng `python` luôn do Claude chạy (danh sách cấm chặn) |
| Lệnh ngoài danh sách (ví dụ `flutter config`) | bị chặn | chặn lệnh đứng riêng; phần nối thêm sau `;`, `&&`, dấu gạch đứng, `>` vẫn lọt (đo 2026-11-16, xem dưới) |

- Đã chạy thật trong Qoder với danh sách cho phép: `flutter create`, `pub add`, `pub get`, `analyze`, `test` và `build apk --debug` (151 s). Lần build đầy đủ đầu tiên có thể lâu hơn (ước lượng 5-8 phút từ lần dựng thử, chưa đo trong luồng thật). Công cụ shell của Qoder **không** timeout ở lệnh build. `flutter analyze` khoảng 11 s, `flutter test` khoảng 5 s.

**Cách cấp lệnh:** một cờ `--allowed-tools "Bash(<lệnh đầy đủ>:*)"` cho mỗi tiền tố lệnh. Khớp theo tiền tố, nên phải liệt kê từng lệnh con: `Bash(D:/flutter/bin/flutter.bat analyze:*)`, `Bash(D:/flutter/bin/flutter.bat test:*)`, `Bash(D:/flutter/bin/flutter.bat pub get:*)`, `Bash(D:/flutter/bin/flutter.bat pub add:*)`, `Bash(D:/flutter/bin/flutter.bat create:*)`, `Bash(D:/flutter/bin/flutter.bat build apk:*)`. Không cấp tiền tố rộng như `flutter.bat` trần (nó sẽ cho phép cả `config`, `upgrade`, `doctor --android-licenses`). Đây là danh sách cho phép hẹp, không phải chế độ `bypass_permissions`, nhưng tiền tố lệnh không phải ranh giới bảo mật (đo 2026-11-16, xem đoạn dưới). `pub add` chỉ dùng cho gói ADR-015 và task file `P<N>.md` phải ghi đúng tên gói; `create` chỉ cấp cho phase tạo dự án; không cấp sẵn mọi lệnh con cho mọi phase. Khớp theo tiền tố chỉ xét phần đầu lệnh; lệnh nối có thể lọt qua cổng cho phép (đã đo 2026-11-16, xem đoạn dưới).

**Đo ngày 2026-11-16: danh sách cho phép không phải sandbox.** Quy tắc `--allowed-tools "Bash(<tiền tố>:*)"` chỉ khớp phần **đầu** của lệnh: nối thêm bằng `;`, `&&`, `|` hay chuyển hướng `>` vẫn qua cổng và chạy lệnh thứ hai; còn `$(...)`, `&` và tiền tố giả mạo (`git statusx`) thì bị chặn. Ngược lại, quy tắc `--disallowed-tools` áp cho **mọi phần** của lệnh nối (cấm `hostname` chặn được `git --version; hostname`, cả bản `&&` và `|`). Vậy danh sách cho phép là rào chắn chống nhầm lẫn, **không phải ranh giới bảo mật**. Giảm rủi ro (đã áp dụng): chỉ cấp đúng các lệnh con flutter cần cho phase kèm một danh sách cấm rộng; không bao giờ cấp `adb`, `emulator`, `docker` cho Qoder; Claude kiểm `git status` và diff sau mỗi phase. Danh sách cấm đã dùng: các lệnh con git `add`, `commit`, `push`, `pull`, `fetch`, `switch`, `checkout`, `reset`, `restore`, `clean`, `stash`, `rebase`, `merge`, `branch`, `tag`, `rm`, `mv`, `config`, `remote`; rồi `gh`, `docker`, `adb`, `emulator`, `wsl`, `rm`, `rmdir`, `del`, `Remove-Item`, `Move-Item`, `Copy-Item`, `curl`, `wget`, `Invoke-WebRequest`, `Start-Process`, `cmd`, `powershell`, `pwsh`, `bash`, `sh`, `python`, `node`, `npm`, `npx`, `setx`, `reg`, `taskkill`, `Stop-Process`, `winget`, `sdkmanager`, `qodercli`, `Set-Content`, `Out-File`, `Add-Content`, `iex`, `Invoke-Expression`, `move`, `copy`, `xcopy`, `robocopy`, `rd`, `ri`, `erase`. Cũng đo được: Qoder báo sai cỡ APK (267,6 MB, thực 188 MB), nên cỡ và các số đo khác phải do Claude đo lại.

**Danh sách cấm là blacklist có lỗ hổng đã biết.** Các lệnh ghi/xóa file `Set-Content`, `Out-File`, `Add-Content`, `iex`/`Invoke-Expression`, `move`, `copy`, `xcopy`, `robocopy`, `rd`, `ri`, `erase` trước đây không có trong danh sách (nay đã thêm ở trên); `flutter.bat config` vẫn không bị cấm; `git -C . push` có thể không khớp quy tắc cấm "lệnh con git" (tiền tố là `git -C`, không phải `git push`); và Claude chỉ thấy thay đổi trong repo (`git status`, `git diff`), không thấy lệnh ghi ngoài repo. Vậy danh sách cấm **giảm nhầm lẫn**, chứ **không** làm Qoder an toàn trước cố ý lạm dụng. `dart` cố ý không nằm trong danh sách cấm vì phase drift cần `dart run build_runner` (chỉ cấp hẹp khi cần).

**Thực tế khi gọi:**

- (a) Đặt việc vào `.ai-work/ST-xx/P<N>.md` và gọi Qoder bằng prompt một dòng "Read <file> and carry out exactly what it says" (tránh việc PowerShell tách sai tham số với prompt dài).
- (b) `-w` phải là thư mục mà lệnh cần chạy trong đó (với `flutter pub/analyze/test` là `mobile/`), rồi thêm `--add-dir "d:/project AI/.ai-work/ST-xx"` để Qoder đọc được task file.
- (c) Đặt `PUB_CACHE=D:/flutter_pub_cache` và `GRADLE_USER_HOME=D:/gradle_home`, rồi thêm `D:/flutter/bin` vào PATH của tiến trình PowerShell gọi Qoder **trước** khi khởi động Qoder (tiến trình con kế thừa; PATH của một phiên đang chạy đã cũ). Thiếu `GRADLE_USER_HOME` thì Gradle tạo bản cache thứ hai ở ổ C (đã thấy 6 GB ngày 2026-11-15).
- (d) Luôn dùng đường dẫn đầy đủ `D:/flutter/bin/flutter.bat`.
- (e) Công cụ Edit của Qoder có thể ghi lại file với CRLF trong bản làm việc; với `core.autocrlf=true` Git lưu LF, nên kiểm `git ls-files --eol` trước khi commit.
- (f) Lệnh chạy lâu (build): ghi trong task file "chạy ở foreground, đợi xong, không chuyển sang chạy nền". Qoder `-p` đã thoát khi còn tác vụ nền (ST-01 phase 7: chỉ báo `analyze` và `test`, build vẫn chạy sau đó); gặp vậy Claude tự chạy lại lệnh kiểm và ghi vào workflow-log.

**Ma trận giao việc:**

- **Qoder:** mọi việc sửa file; `flutter create`, `pub add`, `pub get`, `analyze`, `test`, `build apk`; đọc git chỉ đọc; tự sửa lỗi analyze/test tối đa 3 vòng.
- **Claude:** viết task file `P<N>.md`, gọi Qoder, kiểm kết quả bằng lệnh ngắn (vài dòng cuối), mọi lệnh git ghi (`add`, `commit`, `push`), `gh` (PR, review), subagent review, quyết định và hỏi chủ dự án. Claude chỉ tự chạy `flutter create`/`build`/`pub` khi Qoder không làm được (timeout, lỗi môi trường) và ghi lý do vào [workflow-log.md](workflow-log.md); Claude vẫn chạy lại `flutter analyze` và `flutter test` bằng lệnh ngắn để kiểm (mục 4). `adb` chỉ do Claude chạy và luôn kèm `-s <serial>` (ví dụ `-s emulator-5554`); Qoder không bao giờ được cấp `adb`, `emulator` hay `docker`.

Ví dụ một lần gọi (PowerShell):

```powershell
$env:PUB_CACHE = "D:/flutter_pub_cache"
$env:GRADLE_USER_HOME = "D:/gradle_home"
$env:PATH = "D:/flutter/bin;" + $env:PATH
# --disallowed-tools: một cờ cho mỗi mục của danh sách cấm ở trên (ví dụ vài mục dưới, không lặp cả danh sách)
qodercli -p -w "d:/project AI/mobile" --add-dir "d:/project AI/.ai-work/ST-xx" -n "ST-xx-p<N>" --permission-mode accept_edits --allowed-tools "Bash(D:/flutter/bin/flutter.bat analyze:*)" --allowed-tools "Bash(D:/flutter/bin/flutter.bat test:*)" --disallowed-tools "Bash(git add:*)" --disallowed-tools "Bash(git commit:*)" --disallowed-tools "Bash(git push:*)" --disallowed-tools "Bash(gh:*)" --disallowed-tools "Bash(docker:*)" --disallowed-tools "Bash(adb:*)" --append-system-prompt "Follow AGENTS.md; never run git write commands or gh; edit only the files in the task file; never type a backslash" "Read d:/project AI/.ai-work/ST-xx/P<N>.md and carry out exactly what it says."
```

Khi làm bằng worktree (mục 2b), thay `d:/project AI` bằng thư mục worktree `d:/project AI_wt/ST-xx`.

#### Cài đặt ngoài repo

- Mọi thứ cài hoặc tải ngoài thư mục repo phải ghi vào [machine-installs.md](machine-installs.md) trong cùng PR.
- Dự án thử và bản clone do subagent tạo phải nằm ở ổ D (ví dụ `D:/project AI_tmp/`) và xóa ngay khi xong nếu được; nếu cơ chế an toàn chặn lệnh xóa thì báo chủ máy tự xóa.
- Không đóng hay gỡ ứng dụng, phiên làm việc của chủ máy.
- Không sửa `.wslconfig`.
- Docker do chủ máy bật thì giữ nguyên trạng thái khi tiếp quản.
- Số đo Qoder báo (dung lượng, thời gian) phải được Claude đo lại.

## 4. Claude kiểm sau mỗi lần Qoder chạy

```bash
git status --short          # chỉ có file trong danh sách cho phép
git diff --stat
git log -1 --oneline        # không có commit lạ
git status --short --ignored mobile   # file mới bị .gitignore bỏ qua sót?
cd mobile && flutter analyze && flutter test
```

Khối này chạy bằng Git Bash; các khối khác trong tài liệu là PowerShell 5.1 (không có `&&`).

- Chạy lệnh kiểm ngắn (chỉ lấy vài dòng cuối), ví dụ `flutter analyze` và `flutter test` với `| tail -3`, để tiết kiệm token; đọc đầy đủ chỉ khi lệnh lỗi.
- File ngoài danh sách bị sửa → `git restore <file>`, báo Qoder.
- Có commit hoặc nhánh lạ → dừng, báo chủ dự án.
- Test mới phải **fail trước khi sửa và pass sau khi sửa** (với logic ở `core/domain`).
- Story có màn hình → chạy trên emulator, chụp màn hình vào `.ai-work/ST-xx/evidence/`. Tắt emulator khi xong; server Docker dùng chung thì để chạy (mục 4b).

### 4b. Chạy máy giả lập (Claude làm, không giao Qoder)

Qoder ở `accept_edits` mặc định không chạy được `python` và `flutter` (đo 2026-11-15, cổng quyền chặn); với danh sách cho phép hẹp thì chạy được `flutter` (mục 3b). Việc mở máy giả lập, cài app, chụp màn hình và dọn dẹp **đã chạy thật ngày 2026-11-16** (ST-01.3) và do **Claude** làm, không giao Qoder: Qoder không bao giờ được cấp `adb`, `emulator` hay `docker` (mục 3b). AVD của chủ máy chỉ chạy `-no-snapshot -read-only` và gỡ app sau khi thử; camera giữ `virtualscene` vì máy dev không có webcam. Prompt giao Qoder không yêu cầu mở emulator, và không nâng quyền để lách (mục 3).

| Mục | Giá trị trên máy dev (kiểm 2026-11-15 và 2026-11-16) |
|---|---|
| AVD | `pixel_7_-_api_36_0` (chính; chạy `-no-snapshot -read-only`, gỡ app sau khi thử), `Medium_Phone_API_37.0` (không dùng: chưa chạy lần nào, sẽ thêm khoảng 10 GB ổ C); `emulator -list-avds` ra đúng hai tên này |
| Thư mục AVD | `$env:USERPROFILE/.android/avd/` |
| Android SDK | `$env:LOCALAPPDATA/Android/Sdk`; có `emulator/emulator.exe` và `platform-tools/adb.exe`; **chưa** có trong PATH, `ANDROID_HOME` chưa đặt |
| Flutter | `D:/flutter/bin/flutter.bat` |
| Camera | giữ `virtualscene` (mặc định AVD `pixel_7_-_api_36_0`): máy dev không có webcam (`emulator -webcam-list` rỗng, đo 2026-11-16). Máy có webcam thì thêm cờ `-camera-back webcam0`; kiểm thật ở ST-12.1/ST-25.3 |
| Server AI | Chạy bằng `docker compose up` (kiểm bằng `GET /health`, cổng 8000); app gọi `http://10.0.2.2:8000` — đã kiểm 2026-11-16: hiện "Đã kết nối (final-2026-11-08)"; tắt container thì hiện "Chưa kết nối được", bật lại thì hồi |

Quy trình (PowerShell; lệnh **đã chạy thật** trên máy này ngày 2026-11-16, ST-01.3). Kiểm số emulator trước và sau khi mở; dùng đúng serial mà `adb devices` in ra, không ghim cứng `emulator-5554`:

```powershell
$sdk = "$env:LOCALAPPDATA/Android/Sdk"
# (a) TRƯỚC khi mở: adb devices phải KHÔNG có dòng emulator-* nào. Nếu đã có một dòng (AVD có sẵn của chủ máy, Android Studio, dự án khác) → DỪNG, hỏi chủ máy (mục 7); không kill, không dùng lại.
& "$sdk/platform-tools/adb.exe" devices
# (b) mở emulator, gán tiến trình vào biến để giữ PID
$p = Start-Process "$sdk/emulator/emulator.exe" -ArgumentList '-avd','pixel_7_-_api_36_0','-no-snapshot','-read-only','-no-audio','-no-boot-anim' -PassThru   # giữ PID; AVD có sẵn của chủ máy: không nạp/lưu snapshot
# sau khi mở, adb devices in ra serial emulator-*; gán đúng serial đó vào $serial (không ghim cứng)
& "$sdk/platform-tools/adb.exe" devices
$serial = "emulator-5554"   # ví dụ: thay bằng đúng serial mà adb devices vừa in ra
# boot xong chưa? lặp lệnh dưới tới khi in ra 1 (chưa xong thì in rỗng hoặc 0; máy này boot khoảng 30 s)
& "$sdk/platform-tools/adb.exe" -s $serial shell getprop sys.boot_completed      # 1 = đã khởi động xong
# (c) SAU khi boot: adb devices phải có ĐÚNG MỘT dòng emulator-* (là máy mình, vì trước đó không có dòng nào)
& "$sdk/platform-tools/adb.exe" devices
& "$sdk/platform-tools/adb.exe" -s $serial emu avd name   # (chưa thử) kiểm thêm: phải in ra pixel_7_-_api_36_0
# (d) chỉ sau (c) mới chạy các lệnh dưới, tất cả kèm -s $serial
# cài APK debug đã build bằng `flutter build apk --debug` (không dùng `flutter run`/`flutter install`); đường dẫn tính từ thư mục gốc repo hoặc worktree
& "$sdk/platform-tools/adb.exe" -s $serial install -r mobile/build/app/outputs/flutter-apk/app-debug.apk
& "$sdk/platform-tools/adb.exe" -s $serial shell am start -n vn.medicheck.mobile/.MainActivity
New-Item -ItemType Directory -Force "d:/project AI/.ai-work/ST-xx/evidence" | Out-Null
& "$sdk/platform-tools/adb.exe" -s $serial shell screencap -p /sdcard/x.png
& "$sdk/platform-tools/adb.exe" -s $serial pull /sdcard/x.png "<đường dẫn đích>"
& "$sdk/platform-tools/adb.exe" -s $serial shell rm /sdcard/x.png   # xóa ảnh trên máy ảo sau khi pull
& "$sdk/platform-tools/adb.exe" -s $serial logcat -d -s flutter:V AndroidRuntime:E
& "$sdk/platform-tools/adb.exe" -s $serial uninstall vn.medicheck.mobile   # gỡ app sau khi thử (AVD của chủ máy)
& "$sdk/platform-tools/adb.exe" -s $serial emu kill                               # (e) chỉ emu kill máy mình đã mở (PID trong $p); không bao giờ kill emulator không phải do mình mở
```

- Chỉ một emulator và một bản app tại một thời điểm (2b.3-6). Chụp xong thì `emu kill`; server Docker dùng chung thì để chạy.
- Không `adb kill-server` (adb dùng chung với IDE khác), không `wsl --shutdown`; mọi lệnh `adb` kèm `-s <serial>` (serial do `adb devices` in ra, không ghim cứng) và chỉ `emu kill` máy mình đã mở.
- Gỡ app sau khi thử là lưới an toàn phòng khi emulator lỡ được mở mà thiếu `-read-only` (AVD có sẵn của chủ máy luôn chạy `-no-snapshot -read-only`).
- Không dán output `logcat` vào nhật ký hay PR nếu nó có thể chứa chữ từ đơn thuốc (BR-10).
- Ảnh chụp chỉ ở `.ai-work/ST-xx/evidence/`, so với `docs/design/png/<màn>.png`; không commit (mục 6).
- Emulator không lên sau khoảng 3 phút, hoặc `flutter` báo lỗi giấy phép Android SDK/PATH → dừng và hỏi chủ dự án (mục 7).
- Ảnh chụp là pixel thật của máy ảo (Pixel 7: 1080×2400 px, khoảng 411×914 dp), không phải khung 390×844 của ảnh chuẩn: so bố cục theo dp và tỉ lệ, không so từng pixel. Muốn đúng 390×844 thì đặt `adb shell wm size` và `adb shell wm density`, xong thì `wm size reset` và `wm density reset` (chưa thử).

## 5. Checklist review (mỗi PR)

- [ ] Đạt tiêu chí chấp nhận của từng FR; TC liên quan đạt.
- [ ] **BR-01:** không có đường nào hiện xanh hay "Tôi đã uống" khi `status != "green"`, kể cả lỗi/timeout.
- [ ] **BR-10 / ADR-016:** không lưu ảnh thuốc; ảnh đơn chỉ ở thư mục app; không log nội dung đơn.
- [ ] **BR-12:** không tạo được 2 đơn `active`.
- [ ] Giao diện khớp ảnh chuẩn `docs/design/png/` (so bố cục theo dp và tỉ lệ với ảnh chuẩn 390 × 844, mục 4b); dùng token, không số rời.
- [ ] Chữ hiển thị chỉ ở `strings_vi.dart`, không có từ cấm; chữ ≥ 20 sp, vùng chạm ≥ 48 dp, có `Semantics`.
- [ ] DTO khớp `openapi.yaml`; `utf8.decode(res.bodyBytes)`.
- [ ] Không thêm thư viện ngoài ADR-015; không sửa `out/onnx_final/`.
- [ ] Docs bị ảnh hưởng đã sửa trong cùng PR.

## 5b. Review PR kĩ càng và cổng merge

Mức: High / Medium / Low (cũ: BLOCKER / MAJOR / MINOR; các comment review cũ trên PR dùng tên cũ).

Review PR là bước **bắt buộc**. Người review (Claude, có thể thêm subagent chạy song song theo trục: đúng yêu cầu · quy tắc BR/ADR · riêng tư và file cấm · tài liệu nhất quán) đọc **diff thật trên GitHub**, không đọc báo cáo tự khai của người viết.

**Prompt review chuẩn** (dán cho Claude hoặc subagent; chỉ đọc, không sửa file, không git ghi, không merge):

```
CHỈ ĐỌC: không sửa file, không lệnh git ghi, chỉ dùng `gh pr diff`, `gh pr view`, `gh pr checks` (đọc); không dùng lệnh gh nào khác (áp dụng cho subagent review; Claude đăng review theo mục 2 bước 8); chỉ trả báo cáo cho người giao.
Review PR #<n> của repo này.
1. Lấy diff thật: gh pr diff <n>; gh pr view <n> --json files,commits,body,headRefOid,reviews.
2. Đối chiếu với: tiêu chí chấp nhận của story trong docs/product/backlog.md; các FR/UC/SCR/TC story trỏ tới;
   AGENTS.md mục "Quy tắc không được phá"; checklist docs/process/ai-workflow.md mục 5.
3. Tìm lỗi THẬT, không bàn phong cách: sai yêu cầu, hồi quy, vi phạm BR-01/BR-10/BR-12/ADR, lộ dữ liệu hoặc file cấm
   (out/onnx_final/, ảnh người dùng, token, .ai-work), tài liệu mâu thuẫn hoặc liên kết hỏng, thiếu test cho logic mới,
   thay đổi ngoài phạm vi story, dòng AI đồng tác giả hay "Generated with" trong commit/PR.
4. Kiểm từng khẳng định trong body PR bằng lệnh hoặc đọc file; không tin lời tự báo cáo. Đọc file ở đầu PR bằng `git show origin/<nhánh>:<đường dẫn>` (người giao đã `git fetch`; kiểm `git rev-parse origin/<nhánh>` bằng headRefOid), không đọc bản trên main hay trong thư mục làm việc (PR có thể sửa chính tài liệu đang dùng để review).
Vòng ≥ 2: đọc comment các vòng trước (reviews), kiểm từng mục đã được sửa thật chưa, và tìm lỗi mới do chính bản sửa gây ra.
5. Dòng đầu báo cáo ghi headRefOid đã review. Trả về danh sách xếp theo mức, mỗi mục: file:dòng · vấn đề · cách sửa ngắn gọn.
   High = sai hoặc hại nếu làm theo, lộ dữ liệu hay file cấm, vi phạm BR-01/BR-10/BR-12/ADR (trước đây gọi BLOCKER). Medium = sai yêu cầu, thiếu việc story phải làm, hoặc mâu thuẫn mà người làm theo sẽ vấp (trước đây MAJOR). Low = nhỏ, bỏ qua cũng không làm hỏng việc (trước đây MINOR). Nếu không có gì: ghi "Không có High/Medium/Low" và liệt kê đã kiểm những gì.
```

**Vòng review:** review → post `gh pr review <n> --comment` (số High/Medium/Low và danh sách) → Qoder sửa → Claude kiểm diff và chạy lại kiểm → commit, push → vòng sau review **lại toàn bộ diff mới**. Tối đa 3 vòng; vòng 3 còn High/Medium thì dừng và hỏi chủ dự án (mục 7). **3 là trần, không phải số vòng bắt buộc:** vòng nào đạt cổng merge (không còn High/Medium và các điều khác của cổng) thì dừng review và merge, không chạy thêm vòng cho đủ 3. **Vòng cuối** = vòng đầu tiên không còn High và Medium (hoặc vòng 3). Low của các vòng trước vẫn sửa cùng lượt với Medium; ở vòng cuối thì Low ghi lý do bỏ, không sửa. Vòng 3 còn High/Medium thì chủ dự án quyết: thêm vòng (đếm lại) hoặc tự merge ngoài luồng. Vòng cuối chỉ còn Low thì ghi lý do bỏ trong comment, không sửa (sửa là thêm commit và phải review lại, điều 7). Comment của mỗi vòng bắt đầu bằng dòng `Vòng <k> · commit <headRefOid> · High <a> · Medium <b> · Low <c>`, rồi kết quả checklist mục 5 (tích hoặc n/a kèm lý do) và những gì đã kiểm.

**Kiểm theo loại PR:** app: `flutter analyze` và `flutter test`; backend: `backend/tests/test_decide.py` và `openapi.yaml` sinh lại không lệch; chỉ docs: liên kết tương đối không hỏng, mã FR/BR/ADR/ST được nhắc đều có định nghĩa, `git diff --check`.

**Cổng merge** (tất cả phải đúng; thiếu một điều thì không merge):

1. Có ít nhất một vòng review theo prompt trên, đã post lên PR, và vòng cuối khớp với commit cuối của nhánh (`headRefOid`).
2. Vòng cuối: **0 High, 0 Medium** (cổng chỉ cần vậy); Low đã sửa hoặc ghi lý do bỏ ngay trong comment review.
3. Checklist mục 5 đã tích; mục không áp dụng ghi "n/a" kèm lý do.
4. Các kiểm theo loại PR (trên) chạy lại trên commit cuối và đạt.
5. `git diff --name-only origin/main...HEAD` (tại cổng nhánh cha đã merge và nhánh con đã `rebase --onto origin/main`, nên luôn dùng `origin/main...HEAD`; `<nhánh-cha>...HEAD` chỉ dùng ở self-review khi cha chưa merge) chỉ có file trong phạm vi story, hoặc phạm vi mở rộng do chủ dự án giao bằng lời và được ghi nguyên văn trong body PR (thay đổi `tasks.csv` và `workflow-log.md` của chính story được coi là trong phạm vi; `docs/process/machine-installs.md` cũng trong phạm vi khi story có cài đặt ngoài repo); commit và PR không có dòng AI đồng tác giả hay "Generated with".
6. PR không phải Draft, không còn thread chưa xử lý; CI xanh nếu đã có (ST-28).
7. Sau vòng review cuối không có commit mới (có thì quay lại một vòng review mới) (ghi nhật ký sau vòng cuối không phải commit trong PR story: dùng LOG_PENDING.md, mục 8.3).

Merge kiểu squash (lệnh merge: `gh pr merge <n> --squash`). Người merge là chủ dự án; Claude chỉ merge khi chủ dự án đã cho phép bằng lời cho **đúng PR đó**, và ghi nguyên văn câu cho phép vào comment tổng kết của PR. Cổng chưa đạt thì Claude không merge, kể cả khi được nhờ; chủ dự án tự merge trên GitHub là quyền của chủ dự án, ngoài luồng này. Comment tổng kết = một `gh pr comment <n>` đăng sau vòng review cuối, ghi nguyên văn câu cho phép merge của chủ dự án; đây không phải commit.

## 6. Git

- Nhánh: `story/ST-xx-<mo-ta>`, sửa lỗi `fix/<mo-ta>`, tài liệu `docs/<mo-ta>`. Một nhánh một story.
- Commit: `<type>(ST-xx): <tóm tắt>`; `type` ∈ `feat|fix|refactor|test|docs|chore`; tiếng Anh, mệnh lệnh, ≤ 20 từ. Một commit một thay đổi logic.
- Chỉ `git add <đường dẫn cụ thể>`; không `git add -A`, `git add .`, `git commit -a`. Trước khi commit: `git diff --cached --name-only` chỉ chứa file trong phạm vi.
- Không push thẳng `main`; không force-push `main`; `--force-with-lease` chỉ trên nhánh của chính mình.
- Không có dòng `Co-Authored-By` hay "Generated with" của AI trong commit, PR, review.
- Không commit `.ai-work/`, ảnh bằng chứng, `*.db`, token, `build/`, `.dart_tool/`.

## 7. Dừng và hỏi chủ dự án khi

- Một lỗi sửa quá 3 vòng, hoặc sau vòng 3 vẫn còn High/Medium.
- Chủ dự án bảo Claude merge nhưng cổng (mục 5b) chưa đạt, hoặc chưa có lời cho phép merge cho đúng PR đó: dừng, nói rõ điều nào chưa đạt, để chủ dự án quyết.
- Cần sửa docs (trừ `tasks.csv` ở bước 6 hoặc 2b.3-8, `workflow-log.md` ở mục 8 và `docs/process/machine-installs.md` khi story cài thứ gì ngoài repo), thêm thư viện, đổi `pubspec.yaml` ngoài plan, đổi API server.
- Docs mâu thuẫn nhau, hoặc gặp `OQ-xx` chưa chốt.
- Qoder sửa ngoài phạm vi hay chạy lệnh git.
- Sự cố mức **S1** (mục 8.2): dừng, báo, ghi vào [workflow-log.md](workflow-log.md) rồi mới tiếp tục (đã qua bước 6 của mục 2 thì ghi vào `LOG_PENDING.md`, mục 8.3).

## 8. Nhật ký vận hành: ghi lại để luồng ngày càng an toàn và hiệu quả

Mọi trục trặc trong luồng Claude + Qoder (và cả việc chạy 2–3 story cùng lúc) được ghi vào [workflow-log.md](workflow-log.md), xử lý, rồi đưa bài học thành luật. Mục đích: cùng một lỗi không xảy ra hai lần.

### 8.1 Ghi khi nào

Ghi **ngay lúc xảy ra** (không đợi cuối ngày) khi:
- lệnh hoặc công cụ không chạy như kỳ vọng (ví dụ Qoder không chạy được `flutter`);
- Qoder làm sai luật hoặc ra ngoài phạm vi (sửa file không được giao, chạy lệnh git, thêm thư viện);
- xung đột, rebase lỗi, mất việc, commit nhầm nhánh hoặc nhầm worktree, file mới bị `.gitignore` bỏ qua;
- cùng một loại lỗi phải sửa quá một vòng;
- một bước của quy trình gây chậm hoặc rủi ro mà đáng ra tránh được;
- phát hiện một cách làm tốt đáng giữ.

### 8.2 Ghi cái gì

Một dòng trong bảng, đủ để người khác hiểu và làm lại:

| Cột | Nội dung |
|---|---|
| Ngày, story | `2026-11-20`, `ST-07` |
| Mức | **S1** suýt mất việc / lộ file cấm / commit sai nhánh (dừng và báo ngay); **S2** mất thêm ≥ 1 vòng làm lại; **S3** gợi ý cải tiến, cách làm tốt |
| Tình huống | Chuyện gì xảy ra, kèm lệnh hoặc lỗi nguyên văn ngắn |
| Nguyên nhân | Vì sao (nếu chưa biết ghi "chưa rõ") |
| Cách xử lý | Đã làm gì để qua việc |
| Luật liên quan | Mục nào của file này (hoặc "chưa có") |
| Trạng thái | `Đã xử lý` · `Đề xuất luật` · `Đã áp dụng (mục x)` · `Theo dõi` |

Không ghi token, nội dung đơn thuốc thật hay dữ liệu cá nhân.

### 8.3 Quy trình xử lý

1. Claude ghi dòng ngay, trạng thái `Đã xử lý` nếu đã qua việc trong phạm vi luật hiện có, hoặc `Theo dõi` nếu chưa chắc; nếu đã qua bước 6 của mục 2 thì ghi vào `.ai-work/ST-xx/LOG_PENDING.md` (không commit) và gom vào nhật ký ở PR docs kế tiếp, vì thêm commit sau vòng review cuối sẽ kéo thêm một vòng (mục 5b điều 7).
2. Nếu cần **đổi luật** (thêm cấm, đổi cách làm): ghi `Đề xuất luật` và **hỏi chủ dự án**; đồng ý thì sửa file này (ghi số mục) và đổi trạng thái thành `Đã áp dụng`. Không tự đổi luật cứng.
3. Lỗi **cùng loại xuất hiện lần thứ hai** mà chưa có luật: báo chủ dự án và đề xuất luật ngay.
4. **S1 → dừng việc đang làm**, báo chủ dự án trước khi tiếp tục.
5. **Cuối mỗi story:** Claude thêm 1–3 dòng nhìn lại (gì trục trặc, gì tốt, đề xuất đổi gì) vào `workflow-log.md`, trong cùng commit với đổi trạng thái `Done`: ở commit trước vòng review 1 trong PR story, hoặc trong PR docs nhỏ sau merge khi chạy song song (mục 2 bước 6 hoặc 2b.3-8).
6. **Cuối mỗi mốc** (M1, M2, …): Claude rà toàn bộ nhật ký, gom các lỗi lặp, các mục `Đề xuất luật` chưa duyệt, và đề xuất một danh sách cải tiến ngắn.

### 8.4 Dùng nhật ký

Đầu mỗi session code, Claude đọc `Theo dõi` và `Đề xuất luật` còn mở để không lặp lại sai lầm cũ.
