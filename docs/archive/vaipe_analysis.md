# Phân tích dataset VAIPE_PILL (khám phá thực tế, 2026-10-31)

> Nguồn: `Elfsong/VAIPE_PILL` trên Hugging Face, tải về `data/`. Script tái lập: `scripts/` (chạy bằng `.venv`). Số liệu trung gian: `out/` (`class_stats.csv`, `pres_drug_lines.csv`, `pill_images_train.parquet`, `pill_boxes_train.parquet`, ảnh crop theo lớp ở `out/sheets/`).
>
> File này chỉ ghi **sự thật quan sát được** về dữ liệu. Quyết định dựa trên các sự thật này nằm ở `MediCheck_decisions.md`.

---

## 1. Cấu trúc dataset

| Config | Split | Số mẫu | Trường | Ghi chú |
|---|---|---|---|---|
| `pill` | train | 9,502 ảnh | `image`, `filename`, `bboxes` [x,y,w,h], `labels` | ~22GB |
| `pill` | test | 1,500 ảnh | như trên | **Không có bbox lẫn nhãn** (đã kiểm 1 shard: 84 ảnh, 0 box) |
| `prescription` | train | 1,173 đơn | `image`, `texts`, `ann_labels`, `boxes` [x1,y1,x2,y2], `mappings` | Annotation theo từng ô chữ |
| `prescription` | test | 172 đơn | như trên | **Annotation rỗng** |
| `pill_pres_map` | train/test | 9,502 / 1,500 | `prescription` ↔ `pill` | Mỗi ảnh pill thuộc đúng 1 đơn |

- Tên file: ảnh pill `VAIPE_P_{pid}_{k}.jpg` ↔ đơn `VAIPE_P_TRAIN_{pid}.png`.
- `ann_labels` của đơn: `drugname` 2,844 · `quantity` 2,844 · `usage` 3,994 · `diagnose` 1,650 · `date` 1,173 · `other` 28,703.
- `mappings`: mỗi ô `drugname` có class_id của viên thuốc (0–106); mọi ô khác = -1. **2,844/2,844 dòng thuốc đều có mapping** → mọi thuốc trong đơn train đều thuộc 107 lớp.

**Hệ quả:** quan hệ "tên trên đơn → class viên" là **nhãn do tác giả VAIPE gán** (qua `mappings`), không phải suy ra từ đồng xuất hiện.

---

## 2. Ảnh viên thuốc (pill, train)

### 2.1. Số lượng

| Hạng mục | Giá trị |
|---|---|
| Ảnh | 9,502 |
| Box | 32,828 |
| Box class 0–106 | 24,430 |
| Box class 107 | 8,398 (25.6%) |
| Box/ảnh | mean 3.45, median 3, max 11, min 1 |
| Ảnh chỉ toàn 107 | 1,628 · ảnh không có 107: 7,618 · lẫn cả hai: 256 |
| Cùng 1 class xuất hiện ≥2 lần trong 1 ảnh | 6,674 / 17,404 cặp (ảnh, class); tối đa 5 viên |
| Ảnh/đơn | mean 8.1, median 6, max 132 |

### 2.2. Ảnh — kích thước, xoay, thiết bị

- **Kích thước không đồng nhất:** 4032×3024 (2,669), 3024×4032 (2,265), 4000×3000 (1,599), 4128×3096 (1,242), 4624×3468 (404), và nhiều ảnh nhỏ: 960×1280, 720×960, 1280×960, **302×403** (90 ảnh)…
- **EXIF orientation**: 1 → 4,855 · **6 → 4,217** · 3 → 311 · 8 → 58 · 0 → 61. Hơn nửa ảnh cần xoay.
- **Bbox nằm trong hệ toạ độ ĐÃ xoay theo EXIF** (kiểm bằng mắt: vẽ box lên ảnh gốc → lệch hoàn toàn; sau `ImageOps.exif_transpose` → khớp). Pipeline đọc ảnh/train phải exif-transpose trước khi dùng bbox.
- Sau xoay, 77% ảnh dọc.
- Thiết bị: Samsung A22/A20/A70/A52, iPhone 12 Pro/6s/XS Max/7/X… và 1,278 ảnh không có EXIF.
- 11 box vượt biên ảnh vài pixel.

### 2.3. Box

- Kích thước median ~470×471 px; tương đối so với ảnh: cạnh box ≈ **14.5%** cạnh ảnh (p5 = 8%, p95 = 24%).
- Nền (xem `out/sheets/images_*.jpg`): lòng bàn tay, bàn gỗ, giấy kẻ ô, giấy màu xanh lá, vải, nền đen, thảm hoạt hình. Ánh sáng rất khác nhau, có ảnh chói/loá.

### 2.4. Class 107

- Crop class 107 (`out/sheets/class_107.jpg`) là các viên **đa dạng, không trùng các lớp 0–106** (Nospa, Amferu, viên nang mềm, thuốc có chữ dập lạ…).
- 99.8% box lớp 0–106 (24,375/24,430) nằm đúng trong tập class của đơn tương ứng; mọi đơn đều có ít nhất một ảnh chứa viên của đơn.
- → **107 = viên không thuộc đơn của ảnh đó** (quy ước cuộc thi AI4VN 2022; xác nhận qua README các đội thi, ví dụ lynguyenminh/VAIPE2022, cubist38/AI4VN_VAIPE). Lưu ý: 107 **bao gồm cả viên thuộc lớp 0–106 nhưng không nằm trong đơn hiện tại** (ví dụ đơn kê Meloxicam mà ảnh có viên Paracetamol 500 → 107). Viên 107 có thể trông y hệt một lớp đã biết; đây đúng là tình huống "cầm nhầm thuốc khác".
- 55 box lớp 0–106 **không** thuộc đơn của nó, nằm gọn trong 3 đơn: 574 (20), 575 (20), 1168 (15) → nhiễu ở cấp đơn, không phải rải rác.

### 2.5. Phân bố lớp (chi tiết: `out/class_stats.csv`)

- Box/lớp: p10 = 21, p25 = 51, median = 102, p75 = 194, p90 = 565. Max class 64 (2,599), min class 25 và 49 (1 box).
- Lớp < 10 box: **13, 25, 32, 49, 66, 88, 102** (7 lớp). Lớp < 30 box: 14.
- **14 lớp chỉ xuất hiện trong đúng 1 đơn**: 9, 13, 16, 20, 25, 32, 35, 49, 53, 66, **85** (132 box), 86, 94, 102. Một số lớp có nhiều box nhưng toàn bộ đến từ 1 đơn (cùng 1 vỉ thuốc, nhiều ảnh) → ít đa dạng hơn con số box gợi ý.

---

## 3. Đơn thuốc (prescription, train)

### 3.1. Dạng ảnh

- **Ảnh chụp màn hình bản PDF sạch** (có chỉ báo trang "1/1" của trình xem PDF điện thoại; thông tin cá nhân đã che mờ). Không phải ảnh chụp giấy bằng camera: không nghiêng, không bóng, không nhàu.
- Kích thước: 760×1070 (678), 1150×1600 (318), 770×1420 (177).
- **2 mẫu đơn** (cùng 1 hệ thống bệnh viện):
  - **Mẫu A – "TOA THUỐC BHYT"**: 1,030 đơn (88%). Mỗi buổi là 1 ô `usage` riêng ("Sáng 1 Viên", "Tối 2 Viên"), nằm cùng hàng "Ghi chú Uống:" dưới tên thuốc. Có "Số phiếu".
  - **Mẫu B – "ĐƠN THUỐC BHYT"**: 143 đơn (12%). Toàn bộ lịch là 1 ô ("Uống sau khi ăn: Sáng 1 Viên TốI 1 Viên"). Tên thuốc dạng "Hoạt chất (Biệt dược) hàm lượng". Không có "Số phiếu".
- Bài báo SOICT 2023 nói VAIPE_P có 5 mẫu bệnh viện; bản HF này chỉ có 2.
- Năm kê đơn: 2017 (2) · 2018 (199) · 2019 (263) · 2020 (183) · 2021 (494) · 2022 (32).

### 3.2. Dòng thuốc

- Số thuốc/đơn: 1 → 170 · 2 → 482 · 3 → 390 · 4 → 115 · 5 → 16.
- **668 tổ hợp thuốc khác nhau** trên 1,173 đơn (phác đồ lặp lại nhiều).
- ~22 nhóm đơn trùng (cùng ngày + cùng danh sách thuốc, có nhóm 3–4 đơn). Mẫu B không có số phiếu nên không xác định được trùng thật hay khác bệnh nhân.
- Text annotation **gần đúng nhưng không y hệt** chữ trên ảnh (ảnh "150mg, 20mg" ↔ text "150mg+20mg").
- `quantity`: "SL: N Viên" / "SL: N viên" / "SL:N Viên" (đều là đơn vị Viên).

### 3.3. Lịch uống (`usage`)

| Tổ hợp buổi | Dòng thuốc |
|---|---|
| Sáng + Chiều | 1,387 (49%) |
| Chỉ Sáng | 511 |
| Sáng + Tối | 398 |
| **Không có lịch** | **379 (13%)** |
| Chỉ Tối | 113 |
| Sáng+Chiều+Tối | 29 |
| Khác (có Trưa) | 23 |

- **148/1,173 đơn (12.6%) có dòng thiếu lịch; 136 trong số đó thiếu ở MỌI dòng.** Đã kiểm ảnh: dòng "Uống :" thật sự trống, không phải lỗi annotation. Thuốc hay thiếu lịch: Hoạt huyết dưỡng não, Panactol, Kavasdin, Mypara, Novoxim…
- Số viên/buổi: 1 (1,959) · 2 (2,216) · 3 (74) · 4 (19) · 5 (8) · **1/2 (61)** · "1%1/2" (1, lỗi gõ).
- Biến thể chữ: hoa/thường lẫn lộn ("CHIều", "TốI", "TổI", "CHIÊU"), có/không "Viên", tiền tố "Uống:", "Uống sau khi ăn:", "Uống trước khi ăn:", "Cách dùng:".
- **Liều khi cần (PRN)**: "Uống 2v/ lần khi đau. 2 lần uống cách nhau ít nhất 4h" (≥2 dòng).
- Lưu ý ăn uống ở ghi chú: "trước khi ăn" (~139 dòng), "sau khi ăn" (~181 dòng), "ăn N phút".

---

## 4. Mapping tên thuốc ↔ class viên

### 4.1. Đa số quan hệ nhiều-nhiều là biệt dược tương đương

Ví dụ (số dòng đơn):
- class 10 (Amoxicillin 500): FABAMOX 500 (41), NOVOXIM-500 (39), Amoxicilin (Fabamox 500) (38), AMOXICILIN 500MG (32), AMOXICILLIN 500MG (24).
- class 89/91/99 (Paracetamol 500): PANACTOL, PARTAMOL, MYPARA, PARACETAMOL đều map vào cả 3 lớp.
- class 8 (Amlodipine 5): KAVASDIN, PAMLONOR, AMCARDIA, CARDILOPIN.

→ **Tên in trên đơn không xác định duy nhất hình dạng viên**, và cùng tên có thể ra nhiều hình dạng. Phù hợp với thực tế nhà thuốc cấp phát biệt dược tương đương (giả thuyết, chưa có tài liệu xác nhận).

### 4.2. Trong cùng 1 đơn: không có 2 dòng thuốc cùng class

**0/1,173 đơn** có hai dòng thuốc map cùng một class. Tình huống "2 thuốc trong cùng đơn không phân biệt được bằng ảnh" **chưa từng xuất hiện trong dữ liệu train**.

### 4.3. Các lớp khác hoạt chất — kiểm bằng ảnh crop

| Class | Tên trên đơn | Quan sát ảnh crop | Kết luận |
|---|---|---|---|
| 15 / 64 | Atorvastatin ↔ Hoạt huyết dưỡng não | Viên ở class 15 mà đơn ghi "Hoạt huyết" (đơn 119, 120) là viên dập **"AT 20"** (Atorvastatin) | **Lỗi tráo mapping** ở 2 đơn (119, 120 giống hệt nhau); class 15 là Atorvastatin, không gộp 2 thuốc. Đã sửa ở nhãn v2. |
| 1 | TROYSAR AM (12) / TYDOL PM (6) | Troysar: viên dài có logo; Tydol PM: viên xanh nhạt, dập chữ khác hẳn | **2 viên khác hẳn nhau trong cùng 1 lớp** → nhiễu nhãn hoặc lớp không thuần |
| 40 | MEZAFEN/Loxoprofen 60mg (13) / DICLOFENAC 50mg (8) | **Mọi viên** đều tròn cam dập **"50"**, kể cả viên đơn ghi Mezafen | Cùng một viên vật lý; đơn ghi Loxoprofen nhưng viên giống Diclofenac 50 → hoặc nhãn sai, hoặc cấp phát khác hoạt chất (không xác định được) |
| 104 | COSYNDO B (33) / SETBLOOD (22) / SAVI 3B (8) | Viên nang mềm nâu đỏ **nhìn giống hệt nhau**; riêng đơn 401, cả 29 viên ghi Cosyndo B là viên tròn cam (sửa 2026-11-03: trước ghi nhầm là 2 viên) | **Look-alike thật** giữa các thuốc khác thành phần; đơn 401 không xác định được bên nào đúng |
| 37 | DIAMICRON 60mg / 30mg, PYME DIAPRO 30, GOLDDICRON 30 | Lẫn 3 kiểu viên: dập "DIA 30", "DMC", và mũi tên/ngôi sao. Viên đơn ghi "60MG" lại dập "DIA 30" | Lớp **gộp cùng hoạt chất (Gliclazide) nhưng khác hàm lượng và khác ngoại hình** |
| 60 | TYDOL PM (17) / PARACETAMOL 500 (1) | Viên Tydol ở lớp 1 giống hệt viên Tydol ở lớp 60 (cosine 0,983, kiểm 2026-11-03) | Tydol ở lớp 1 là nhãn lệch, đã chuyển sang lớp 60 ở nhãn v2; dòng Paracetamol đơn 708 khả năng nhiễu |
| 2 | DIXIREIN 375mg (52) / Carbocistein (Anpemux) 250mg (13) / ANPEMUX 250mg (1) | Cùng một viên nang vàng cam (kiểm 2026-11-03) | Khác tên và hàm lượng trên đơn, cùng ngoại hình |

### 4.4. Màu sắc không ổn định

Cùng một viên (ví dụ "AT 20" ở class 15; logo Troysar ở class 1) lên ảnh thành **hồng / xanh nhạt / trắng / xám / kem** tuỳ ánh sáng và cân bằng trắng của máy. Màu nhìn thấy trong ảnh **không phải đặc trưng đáng tin** để mô tả viên.

---

## 5. Nguồn gốc dataset và nguồn bổ trợ (kiểm 2026-10-31)

### Bộ hiện tại là gì
`Elfsong/VAIPE_PILL` = bản mirror cá nhân của **dữ liệu cuộc thi AI4VN 2022 "VAIPE: Medicine Pill Image Recognition Challenge"** (public_train + public_test; không có private test). Không phải bộ gốc đầy đủ **VAIPE-Pill** (>50k ảnh) / **VAIPE-P** (~50k đơn, 5 mẫu BV) của VinUni–Illinois Smart Health Center. Khi trích dẫn nên ghi đúng là dữ liệu cuộc thi AI4VN 2022.

### Các nguồn đã kiểm
| Nguồn | Nội dung | Giá trị |
|---|---|---|
| Kaggle `tommyngx/vaipepill2022` (25.2GB, 07/2022) | Gần như chắc là zip gốc của cuộc thi | Trùng bộ hiện tại |
| Kaggle `anhduy091100/vaipe-minimal-dataset` (240MB) | Bộ của bài PLOS ONE 2023: 9,426 ảnh, 96 lớp, ảnh đã thu nhỏ, license Unknown | Nhiều khả năng cùng nguồn, đánh số lớp khác → rủi ro trùng/lệch nhãn |
| GitHub `lynguyenminh/VAIPE2022...` | Code + demo Streamlit, không dữ liệu, không weights | Chỉ có định nghĩa class 107 |
| Kaggle `alexanderyyy/pills-detection-dataset` (1.4GB, CC BY-NC-SA 4.0) | Detection **1 lớp "pill"**, 12,067 ảnh, YOLO format. Bản local: `D:\project AI\dataset bổ sung\` | Bổ trợ được cho **detector**, không cho classifier/OCR |

### Chi tiết bộ alexanderyyy (đã phân tích local)
- Thành phần: VAIPE-reannotated 2,462 ảnh · VAIPE-mosaic ~3,570 (ghép 2×1 từ ảnh VAIPE, một phần đặt tên ẩn danh `mosaic_#`) · **VAIPE-test 1,500 ảnh có bbox (4,771 viên)** · NIH RxImage mosaic ~1,045 · ảnh cá nhân ~1,620 · Negatives 438 (0 viên) · Ultralytics-medical-pills 102 · ảnh web ~650. Có 34 ảnh `VAIPE_PI_#` không có trong bộ HF.
- **So với nhãn gốc (2,426 ảnh trùng tên, 676/1,173 đơn):**
  - Box khớp tốt: IoU median 0.87 (p25 = 0.80). Box mới nhỏ hơn ~11% diện tích (median).
  - **5.3% box gốc rộng quá mức** (box mới < 60% diện tích), tập trung ở vài đơn (1160, 40, 221, 145, 1164…).
  - **151 viên thêm** ở 73 ảnh (1.6% số box). Xem ảnh: phần lớn là **viên nằm ngoài lòng bàn tay** (đống thuốc trên bàn ở rìa ảnh, viên trong túi zip), những viên VAIPE cố ý không gán nhãn.
  - 39 box gốc không có box mới tương ứng.
- **Sửa 2026-11-07 (C4):** VAIPE-reannotated + VAIPE-mosaic thực ra phủ gần toàn bộ ảnh VAIPE train: truy được 9.018/9.502 ảnh (94,9%) bằng tên + perceptual hash + kiểm IoU, kể cả mosaic ẩn danh và ảnh ngang bị tác giả xoay 90°. Chi tiết và cách dùng: `MediCheck_decisions.md` mục 12.2.
- Rủi ro khi gộp: (1) ảnh VAIPE trong bộ này (đã gán lại hoặc ghép mosaic) có thể rơi vào val của mình → rò rỉ; các mosaic đặt tên ẩn danh không truy được nguồn; (2) định nghĩa "viên" khác nhau: VAIPE chỉ gán viên của lượt chụp, bộ này gán mọi viên kể cả ở nền.

## 6. Câu hỏi mở từ khám phá dữ liệu

14 câu hỏi phát sinh từ khám phá (chia train/val, đơn trùng, lớp không thuần, hàm lượng, lớp 107, OCR, đơn thiếu lịch, liều 1/2 và khi cần, trước/sau ăn, tên hay hoạt chất, màu sắc, test không nhãn, bộ bổ trợ, phạm vi detector) **đã chốt ngày 2026-11-03**. Câu trả lời và căn cứ: `MediCheck_decisions.md` mục 6.
