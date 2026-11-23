# GIÁO TRÌNH TOEIC LISTENING — CHƯƠNG 2 (BẢN 2.0 — NÂNG CẤP)

**Mã chương:** CH02
**Tên chương:** Part 1 và Part 2 — nghe thật: mô tả ảnh, âm thanh thực tế, câu hỏi – phản hồi
**Phiên bản nội dung:** 2.0 (thay thế hoàn toàn 1.0)
**Điều kiện mở khóa:** hoàn thành Chương 1 và đạt ≥ 80% bài kiểm tra Chương 1.
**Thời lượng gợi ý:** khoảng 21 buổi (3 tuần), mỗi buổi 30–45 phút: Bài 4 chia 3–4 buổi, các bài còn lại 1–2 buổi, cộng buổi ôn Mistake Book và Final Test.
**Ngân hàng câu luyện mở rộng:** `CHAPTER_02_BANK.md` (110 câu MCQ + 20 dictation + 20 câu số + 24 cặp âm). Mỗi bài dùng các câu trong file này **cộng** các câu mẫu bên dưới.
**Mục tiêu điểm:** nền cho mốc Listening 300. Với Part 1 + Part 2 (31/100 câu Listening), mục tiêu của chương là **≥ 5/6 Part 1 và ≥ 18/25 Part 2** ở tốc độ thật. Mức quy đổi sang điểm thay đổi theo từng đề, nên dùng con số này làm mục tiêu luyện tập chứ không phải cam kết điểm.

> Nội dung do giáo trình tự biên soạn: mô phỏng kỹ năng và dạng bẫy của TOEIC, không phải đề ETS chính thức, không chép sách thương mại.

---

## 0. Triết lý chương: "học xong là nghe được"

Bản 1.0 chỉ dạy **biết đáp án**. Bản 2.0 dạy **nghe được**, gồm 4 lớp:

1. **Âm thanh:** giải mã nối âm, âm yếu, đuôi -ed/-s, số và giờ. Đây là lý do người học "biết từ mà vẫn không nghe ra".
2. **Nhận dạng nhanh:** xác định loại câu hỏi từ 2–3 từ đầu.
3. **Chiến thuật loại trừ:** biết từng loại bẫy và thấy trước chúng.
4. **Vòng sửa lỗi:** mỗi câu sai được gắn **mã lỗi** cụ thể và sinh bài luyện lại đúng điểm sai đó.

**Quy tắc vàng:** một bài chỉ được tính là "đã nắm" khi người học nghe lại **không transcript** ở tốc độ 1.0x và đúng, **sau ít nhất 24 giờ**, không phải chỉ đúng ngay sau khi đọc giải thích.

---

## 1. Chuẩn âm thanh cho web app (giao cho người code)

| Hạng mục | Quy định |
|---|---|
| Giọng | Luân phiên **Mỹ, Anh, Úc, Canada**, nam và nữ, như thực tế bài thi. Mỗi item gắn `accent` và `gender`. |
| Part 1 | Mỗi lựa chọn là **một file audio riêng**, chỉ đọc nội dung câu, **không đọc chữ A/B/C/D** (khớp bài thi: người nghe tự đếm thứ tự). Khoảng nghỉ giữa các câu 0.8–1.2 s. |
| Part 2 | Câu hỏi/câu trần thuật là một file; ba phản hồi là ba file riêng. Mỗi phản hồi nên do **giọng khác** với người hỏi. Khoảng nghỉ giữa các phần khoảng 1 s. |
| Nghe một lần | Chế độ **Thi** chỉ phát một lần, không tua. Chế độ **Học** cho nghe lại, chậm 0.85x, hiện transcript. |
| Tốc độ | Điểm khởi đầu để **hiệu chỉnh**: khoảng **140–160 từ/phút** cho câu Part 2 tự nhiên. Con số này chưa phải thông số chính thức của ETS. Người làm audio cần so với một đề ETS thật rồi chỉnh. Tránh giọng TTS đều đều: cần có ngắt nhịp, trọng âm và ngữ điệu hỏi/khẳng định rõ. |
| Chất lượng | Không đọc chậm từng chữ. Giữ nối âm và âm yếu tự nhiên (xem Bài 4). Nếu TTS không tạo được nối âm, ghi chú vào item để thu/chọn giọng khác. |
| Xáo đáp án | Vị trí đáp án đúng **phải xáo ở runtime**. Bảng đáp án trong file này chỉ là đáp án gốc. Vì mỗi lựa chọn là một file audio riêng, xáo chỉ là thay đổi thứ tự phát. |

---

## 2. Cấu trúc dữ liệu một câu hỏi (cho người code)

Mọi câu MCQ trong chương dùng khung sau. Trường `distractor_code` là **nền tảng của chẩn đoán**.

```
id: CH02-L01-Q01
part: 1 | 2
accent: US-F | UK-M | AU-F | CA-M ...
difficulty: 1-3
image_brief: (Part 1) mô tả ảnh cho Gemini vẽ SVG, không chữ, không logo
visible_facts: (Part 1) những gì chắc chắn thấy trong ảnh
options: [{key, audio_text, correct, distractor_code, why_wrong_vi}]
explanation_vi
skill_tags: [...]
repair_drill: mã bài sửa lỗi (xem mục 3)
```

**Cách chẩn đoán khi người học sai:** app biết người học chọn lựa chọn nào, nên biết ngay mã bẫy họ rơi vào. Quy tắc đơn giản: sai ≥ 2 lần cùng một `distractor_code` → hiện chẩn đoán, và sinh bài luyện lại đúng mã đó (mục 3).

**Về câu hỏi "có thể gửi đáp án cho AI phân tích không":** có thể. Gửi `{item, lựa chọn của người học, thời gian làm, số lần nghe lại, 20 lỗi gần nhất}` đến AI để nhận xét sâu bằng tiếng Việt. Lưu ý: không đặt API key ở trình duyệt, phải qua một backend nhỏ (proxy) và có giới hạn số lần gọi. Phần chẩn đoán theo mã lỗi ở đây **chạy được hoàn toàn không cần AI**; AI chỉ là lớp bổ sung.

---

## 3. Hệ thống mã lỗi và bài sửa lỗi

### 3.1. Mã bẫy ở Part 1

| Mã | Tên bẫy | Biểu hiện | Bài sửa (repair) |
|---|---|---|---|
| P1-ACT | Sai hành động | Đúng người/vật nhưng động từ khác hình | R1: nhận diện động từ từ ảnh |
| P1-ABS | Vật/người không có trong ảnh | Nhắc đến thứ không thấy | R2: danh sách "có thấy / không thấy" |
| P1-LOC | Sai vị trí | Nhầm beside/behind/under/on… | R3: giới từ vị trí |
| P1-PRG | Sai thể/trạng thái | Nhầm wearing/putting on; is being V3 / has been V3 / is V3 | R4: thể và trạng thái |
| P1-INF | Suy diễn quá mức | Thêm nghề nghiệp, mục đích, thời gian | R5: chỉ chọn điều nhìn thấy |
| P1-OPP | Sai chiều/ngược | load/unload, open/close | R6: cặp động từ đối lập |
| P1-SND | Nhầm âm tương tự | Nghe giống nhưng khác từ | R7: cặp âm gần nhau |

### 3.2. Mã bẫy ở Part 2

| Mã | Tên bẫy | Biểu hiện | Bài sửa |
|---|---|---|---|
| P2-WHQ | Sai loại câu hỏi | Trả lời giờ cho câu hỏi nơi chốn… | R8: nhận loại câu hỏi từ 3 từ đầu |
| P2-REP | Lặp từ | Từ trong đáp án trùng từ trong câu hỏi | R9: "bẫy lặp từ" |
| P2-SND | Nhầm âm | copy/coffee, sale/sail… | R7 |
| P2-YNA | Yes/No cho câu hỏi WH | "Where…?" → "Yes, …" | R8 |
| P2-TNS | Sai thì | Hỏi tương lai, đáp quá khứ | R10: thì và mốc thời gian |
| P2-PER | Sai chủ thể | Hỏi "you", đáp về "he" vô lý | R11: chủ thể và đại từ |
| P2-REL | Liên quan chủ đề nhưng không trả lời | Cùng chủ đề, sai chức năng | R12: "trả lời đúng chức năng" |
| P2-ASS | Liên tưởng | doctor → hospital… | R12 |

### 3.3. Mã lỗi nghe (nguyên nhân, không phải bẫy)

Khi người học sai và **nghe lại với transcript thì hiểu**, đó là lỗi nghe, không phải lỗi hiểu nghĩa.

| Mã | Ý nghĩa | Bài sửa |
|---|---|---|
| L-REDUCE | Không giải mã được nối âm/âm yếu | Dictation Bài 4 |
| L-NUM | Nhầm số, giờ, giá | Drill số Bài 4 |
| L-FIRST | Bỏ lỡ 2–3 từ đầu | Drill "3 từ đầu" Bài 5 |
| L-ENDING | Không nghe đuôi -ed/-s | Drill đuôi Bài 4 |
| L-ACCENT | Chỉ nghe được một giọng | Nghe trộn giọng |
| L-MEMORY | Nghe đúng câu hỏi nhưng quên khi tới đáp án C | Luyện nhắc lại mô hình trong đầu (Bài 5) |

### 3.4. Quy trình vòng sửa lỗi

1. Câu sai → ghi vào **Mistake Book** kèm mã lỗi, ngày, giọng.
2. Ngay lập tức: nghe lại ở 0.85x với transcript → **dictation** câu sai → **shadowing** 3 lần.
3. Sinh **3 câu mới cùng mã lỗi**, độ khó bằng hoặc thấp hơn. Cần 3/3 đúng mới qua bài sửa.
4. Ôn lại sau **1 ngày, 3 ngày, 7 ngày** ở 1.0x, không transcript. Đúng cả ba lần thì mã lỗi đó được "đóng".
5. Nếu cùng một mã sai 3 buổi liền → khuyến nghị quay lại bài học chứa mã đó, đọc lại lý thuyết, rồi mới làm tiếp.

---

## 4. Bản đồ chương

| Bài | Nội dung | Kỹ năng chính |
|---|---|---|
| L01 | Part 1: người và hành động | present continuous, wearing/putting on, động từ hành động |
| L02 | Part 1: vị trí, đồ vật, ảnh không người | giới từ vị trí, bẫy "không có người" |
| L03 | Part 1: bị động, trạng thái, bẫy suy diễn | is being V3 / has been V3 / is V3, supported detail |
| L04 | **Nghe thật:** nối âm, âm yếu, đuôi, số và giờ, giọng Anh/Úc | dictation, minimal pairs, number drills |
| L05 | Part 2: nhận loại câu hỏi WH trong 3 từ đầu | WH, bẫy lặp từ và bẫy âm |
| L06 | Part 2: Yes/No, tag, phủ định, lựa chọn | trả lời gián tiếp, "Yes/No" không phải lúc nào cũng có mặt |
| L07 | Part 2: câu hỏi gián tiếp, yêu cầu, lời đề nghị, gợi ý | chức năng giao tiếp |
| L08 | Part 2: câu trần thuật và câu trả lời gián tiếp | statement, "I don't know", chuyển hướng |
| L09 | Part 2: paraphrase và bản đồ bẫy tổng hợp | paraphrase, loại trừ |
| FINAL | Kiểm tra tổng kết | 25 câu mới: Part 1 (6) + Part 2 (19) |

---

# BÀI 1 — PART 1: NGƯỜI VÀ HÀNH ĐỘNG

## Mục tiêu
- Nhìn ảnh và **dự đoán trước** 3–4 từ có thể xuất hiện.
- Nghe động từ chính và `be + V-ing`.
- Phân biệt **đang làm** và **đã/sẽ làm**; **mặc/đeo** và **đang mặc vào**.

## 1.1. Quy trình 5 giây trước khi audio chạy

Trong Part 1 bạn có vài giây nhìn ảnh. Làm đúng ba bước:

1. **Ai/cái gì là trung tâm?** (một người, nhiều người, không có người).
2. **Hành động hay trạng thái?** Có người đang làm gì không? Nếu không có người thì là trạng thái vật.
3. **Đoán trước 3 từ:** ví dụ ảnh người đứng cạnh máy photocopy → *copier, paper, use*.

Khi nghe: đánh dấu mỗi lựa chọn **✓ / ✗ / ?** trong đầu. Chỉ chọn câu **hoàn toàn đúng**. Một từ sai trong câu là loại.

## 1.2. Quy tắc cốt lõi: câu đúng phải đúng 100%

Một câu như *"A man is repairing a printer"* sai dù ảnh có đúng một người đàn ông và đúng một cái máy, vì động từ không khớp. Đây là bẫy phổ biến nhất của Part 1 (**P1-ACT**).

## 1.3. Cặp dễ nhầm (hành động và trạng thái)

| Đúng khi ảnh cho thấy | Sai khi |
|---|---|
| She **is wearing** a coat. (đang mặc sẵn) | She **is putting on** a coat. (đang trong động tác mặc vào) |
| He **is holding** a folder. | He **is picking up** a folder. |
| They **are standing** in line. | They **are standing up**. |
| She **is looking at** a screen. | She **is repairing** a screen. |
| He **is using** a copier. | He **is fixing** a copier. |

Với ảnh một người đứng yên, câu có `wearing / holding / standing / sitting` thường an toàn hơn câu mô tả động tác chuyển tiếp như `putting on / picking up`.

## 1.4. Động từ hành động hay gặp

| Cụm | Nghĩa |
|---|---|
| examine / inspect / check | xem xét, kiểm tra |
| operate / use a machine | vận hành, dùng máy |
| load / unload a truck | chất / dỡ hàng |
| arrange / organize | sắp xếp |
| point at / gesture toward | chỉ vào |
| hand / pass | đưa, chuyển cho |
| lean over / bend over | cúi người |
| push / pull a cart | đẩy / kéo xe |
| shake hands | bắt tay |
| reach for | với tay lấy |

## 1.5. Bài luyện Part 1

> Mỗi ảnh: không chữ, không logo; hành động chính phải rõ.

#### CH02-L01-Q01 · US-M · ★1
**Ảnh:** Một người đàn ông đứng cạnh máy photocopy, đang đặt xấp giấy vào khay.
**Visible:** một người, máy photocopy, xấp giấy. **Không thấy:** máy in đang bị tháo ra, hộp thư.
- A. A man is repairing a printer. `P1-ACT`
- B. A man is using a copier. ✓
- C. A man is stapling some pages. `P1-ACT`
- D. A man is collecting mail from a box. `P1-ABS`

**Giải thích:** Hành động là dùng máy photocopy. A chỉ đúng "người + máy", sai động từ. D thêm vật không có.
**Skill:** `use/operate`, `P1-ACT`.

#### CH02-L01-Q02 · UK-F · ★1
**Ảnh:** Hai phụ nữ mặc đồ công sở bắt tay nhau qua bàn; trên bàn có vài tờ giấy.
**Visible:** hai người, bắt tay, bàn, giấy. **Không thấy:** bút ký, tòa nhà bên ngoài.
- A. They are signing a form. `P1-INF`
- B. They are hanging a picture. `P1-ACT`
- C. They are walking down some stairs. `P1-ACT`
- D. They are shaking hands. ✓

**Giải thích:** "Signing" là suy diễn từ giấy trên bàn, nhưng ảnh không cho thấy ai cầm bút.
**Skill:** `shake hands`, `P1-INF`.

#### CH02-L01-Q03 · AU-M · ★2
**Ảnh:** Một người đội mũ bảo hộ, mặc áo phản quang, cầm bảng kẹp giấy, ngẩng nhìn một tòa nhà đang xây.
**Visible:** mũ bảo hộ, áo phản quang, bảng kẹp giấy, tòa nhà đang xây. **Không thấy:** thang, cần cẩu đang chạy.
- A. A woman is looking at a building. ✓
- B. A woman is climbing a ladder. `P1-ACT`
- C. A woman is driving a crane. `P1-ACT`
- D. A woman is handing out hard hats. `P1-ACT`

**Giải thích:** Câu đúng chỉ mô tả hành động nhìn thấy được. Nghe hard hat dễ kéo sang D.
**Skill:** `look at`, `P1-ACT`.

#### CH02-L01-Q04 · CA-F · ★2
**Ảnh:** Quầy cà phê; nhân viên đưa một ly cho khách; phía sau có vài người xếp hàng.
**Visible:** nhân viên, ly, khách, hàng người. **Không thấy:** bàn ngồi, thực đơn ngoài trời.
- A. Customers are seated at tables. `P1-LOC`
- B. A server is wiping the counter. `P1-ACT`
- C. A server is handing a cup to a customer. ✓
- D. Customers are reading a menu outside. `P1-LOC`

**Giải thích:** Hành động chính là đưa ly (`hand`).
**Skill:** `hand/pass`, `P1-LOC`.

#### CH02-L01-Q05 · US-F · ★3
**Ảnh:** Một người đàn ông mặc áo choàng phòng thí nghiệm, **đã đeo** kính bảo hộ, đang nhìn vào kính hiển vi.
**Visible:** áo choàng, kính bảo hộ (đã đeo), kính hiển vi. **Không thấy:** bảng viết, đồ uống.
- A. A man is writing on a whiteboard. `P1-ACT`
- B. A man is looking into a microscope. ✓
- C. A man is pouring a drink. `P1-ACT`
- D. A man is putting on safety glasses. `P1-PRG`

**Giải thích:** Kính đã được đeo sẵn, nên `putting on` (đang trong động tác đeo vào) sai. Đây là bẫy `wearing` vs `putting on`.
**Skill:** `wearing vs putting on`, `P1-PRG`.

### Tự kiểm tra Bài 1
Đạt khi đúng **≥ 4/5** và nói được lý do loại từng câu sai bằng đúng mã (ACT / ABS / INF / PRG).

---

# BÀI 2 — PART 1: VỊ TRÍ, ĐỒ VẬT VÀ ẢNH KHÔNG CÓ NGƯỜI

## Mục tiêu
- Nghe đúng giới từ vị trí.
- Xử lý ảnh **không có người**: câu đúng thường mô tả vật và vị trí, **không** có hành động của người.

## 2.1. Giới từ vị trí

| Cụm | Nghĩa | Cẩn thận |
|---|---|---|
| beside / next to | bên cạnh | khác `behind` |
| in front of | phía trước | khác `behind` |
| behind | phía sau | |
| on / on top of | ở trên (tiếp xúc) | khác `above` (cao hơn, không chạm) |
| underneath / beneath / under | ở dưới | |
| between | ở giữa hai vật | |
| across from / opposite | đối diện | |
| along | dọc theo | |
| lean against | dựa vào | |
| be positioned / be placed / be set | được đặt | |

## 2.2. Bẫy "ảnh không người"

Nếu ảnh không có người, các lựa chọn như *"A worker is carrying…", "Customers are lining up…"* là sai ngay (**P1-ABS**). Hãy ưu tiên câu mô tả vật: *"Chairs are lined up…", "A lamp is positioned…"*.

Ảnh không người vẫn có thể có `is being V3` nếu có dấu hiệu hành động đang diễn ra. Nếu ảnh không có dấu hiệu, câu `being V3` thường sai.

## 2.3. Bài luyện Part 1

#### CH02-L02-Q01 · UK-M · ★1
**Ảnh:** Một dãy xe đạp đỗ trong giá để xe, trước một tòa nhà gạch; không có người.
**Visible:** xe đạp, giá để xe, tòa nhà gạch. **Không thấy:** người, xích khóa vào cột đèn.
- A. Some bicycles are being repaired. `P1-INF`
- B. A bicycle is propped against a fence. `P1-LOC`
- C. Some bicycles are parked in a rack. ✓
- D. A bicycle is chained to a lamppost. `P1-ABS`

**Giải thích:** Xe đạp nằm trong giá để xe. A suy diễn "đang sửa".
**Skill:** `be parked`, `P1-INF`.

#### CH02-L02-Q02 · US-F · ★1
**Ảnh:** Sảnh khách sạn: một chậu cây đặt giữa hai chiếc ghế bành; có thảm bên dưới.
**Visible:** chậu cây, hai ghế bành, thảm. **Không thấy:** người, quầy lễ tân, thảm cuộn.
- A. A plant is positioned between two armchairs. ✓
- B. Armchairs are stacked against a wall. `P1-LOC`
- C. A rug is rolled up near the entrance. `P1-ABS`
- D. A plant is hanging above a reception desk. `P1-LOC`

**Giải thích:** `between` = ở giữa hai vật.
**Skill:** `between`, `P1-LOC`.

#### CH02-L02-Q03 · AU-F · ★2
**Ảnh:** Một laptop và một cốc cà phê trên bàn gỗ; cốc ở bên phải laptop; sau bàn là cửa sổ có rèm.
**Visible:** laptop, cốc, bàn, cửa sổ có rèm. **Không thấy:** người đang kéo rèm.
- A. A laptop is on the floor. `P1-LOC`
- B. A mug is under a keyboard. `P1-LOC`
- C. Some blinds are being lowered. `P1-PRG`
- D. A mug is beside a laptop. ✓

**Giải thích:** `beside` = bên cạnh. C dùng `being lowered` nhưng không có người hay dấu hiệu đang kéo rèm.
**Skill:** `beside`, `P1-PRG`.

#### CH02-L02-Q04 · CA-M · ★2
**Ảnh:** Phòng kho: các kệ dọc tường, hộp đặt trên kệ; một cái thang dựa ở cuối kệ; không có người.
**Visible:** kệ, hộp trên kệ, thang dựa tường. **Không thấy:** người mang hộp.
- A. Boxes are being carried down a hall. `P1-PRG`
- B. Some boxes are stored on shelves. ✓
- C. A ladder is lying across a doorway. `P1-LOC`
- D. Some shelves are being assembled. `P1-PRG`

**Giải thích:** Hộp nằm trên kệ. Hai câu `being + V3` sai vì không có người làm.
**Skill:** `be stored`, `P1-PRG`.

#### CH02-L02-Q05 · US-M · ★3
**Ảnh:** Khu bàn ngoài trời của quán cà phê, có ô che; không có người.
**Visible:** bàn, ô che, vỉa hè. **Không thấy:** khách, nhân viên, kiosk.
- A. Umbrellas are set up over some tables. ✓
- B. Customers are lining up at a kiosk. `P1-ABS`
- C. A waiter is wiping the tables. `P1-ABS`
- D. Tables are stacked inside a shop. `P1-LOC`

**Giải thích:** Ảnh không người → loại mọi câu có người. Câu đúng mô tả ô che và bàn.
**Skill:** `no-people image`, `P1-ABS`.

### Tự kiểm tra Bài 2
Đạt khi **≥ 4/5** và nhận ra được ngay câu nào đang "bịa người".

---

# BÀI 3 — PART 1: BỊ ĐỘNG, TRẠNG THÁI VÀ BẪY SUY DIỄN

## Mục tiêu
- Phân biệt `is being V3`, `has/have been V3`, `is/are V3`.
- Không chọn câu thêm thông tin mà ảnh không xác nhận.

## 3.1. Ba cấu trúc bị động và dấu hiệu trong ảnh

| Cấu trúc | Ý nghĩa | Dấu hiệu trong ảnh |
|---|---|---|
| `is/are being + V3` | đang được làm | thấy **người đang tác động** lên vật |
| `has/have been + V3` | đã xong, thấy kết quả | vật ở trạng thái hoàn tất, thường không có người |
| `is/are + V3` | trạng thái | vật đang ở vị trí/trạng thái (stacked, parked, displayed) |

Ví dụ: ảnh thấy công nhân cầm cọ sơn hàng rào → *The fence is being painted.* Ảnh thấy hàng rào đã sơn xong, không người → *The fence has been painted.*

## 3.2. Bẫy suy diễn (P1-INF)

Ảnh một người cầm hồ sơ trước cửa văn phòng. Bạn **không** thể kết luận: *ký hợp đồng, đi phỏng vấn, làm luật sư*. Quy tắc: nếu bạn phải "đoán" để biến câu thành đúng, đó là câu sai.

## 3.3. Cặp đối lập (P1-OPP)

load ↔ unload · open ↔ close · enter ↔ exit · lift ↔ lower · put on ↔ take off. Nghe kỹ tiền tố/động từ chính.

## 3.4. Bài luyện Part 1

#### CH02-L03-Q01 · UK-F · ★1
**Ảnh:** Hai công nhân dùng cọ sơn một hàng rào gỗ thành màu trắng.
**Visible:** công nhân, cọ, hàng rào đang sơn dở.
- A. A fence has been torn down. `P1-INF`
- B. Workers are climbing over a fence. `P1-ACT`
- C. A fence is covered with posters. `P1-ABS`
- D. A fence is being painted. ✓

**Giải thích:** Thấy người đang sơn → `is being painted`.
**Skill:** `is being V3`.

#### CH02-L03-Q02 · AU-M · ★2
**Ảnh:** Các bàn trong nhà hàng đã bày sẵn đĩa, ly, khăn gấp; không có người.
**Visible:** bàn, đĩa, ly, khăn. **Không thấy:** người phục vụ, khách.
- A. A waiter is clearing the plates. `P1-ABS`
- B. Some tables have been set for a meal. ✓
- C. Diners are being seated. `P1-ABS`
- D. A menu is being printed. `P1-ABS`

**Giải thích:** Không người + trạng thái hoàn tất → `have been set`.
**Skill:** `has/have been V3`.

#### CH02-L03-Q03 · US-F · ★3
**Ảnh:** Một người đàn ông cầm một tập hồ sơ, đứng trước cánh cửa văn phòng đóng, nhìn đồng hồ đeo tay.
**Visible:** tập hồ sơ, cửa đóng, đồng hồ. **Không thấy:** người khác, tay đang gõ cửa, bút ký.
- A. A man is signing a contract. `P1-INF`
- B. A man is knocking on a door. `P1-ACT`
- C. A man is holding a folder. ✓
- D. A man is interviewing a candidate. `P1-INF`

**Giải thích:** Chỉ "cầm hồ sơ" là xác nhận được. Mọi câu về mục đích đều suy diễn.
**Skill:** `P1-INF`.

#### CH02-L03-Q04 · UK-M · ★2
**Ảnh:** Xe tải mở cửa sau; hai công nhân đang nâng một thùng hàng xuống khỏi xe.
**Visible:** xe tải, thùng, hai công nhân, thùng đang được chuyển xuống. **Không thấy:** vỉa hè đầy hộp.
- A. A crate is being unloaded from a truck. ✓
- B. A truck is being washed. `P1-ACT`
- C. A crate has been loaded onto a truck. `P1-OPP`
- D. Boxes are piled on a sidewalk. `P1-ABS`

**Giải thích:** `unload` ≠ `load`. Chú ý tiền tố **un-**.
**Skill:** `load/unload`, `P1-OPP`.

#### CH02-L03-Q05 · CA-F · ★3
**Ảnh:** Nhiều đèn treo thả từ trần cao trong một sảnh; không có người.
**Visible:** đèn treo, trần cao, sảnh. **Không thấy:** người lắp đèn, thang.
- A. Some lamps are being installed by a worker. `P1-ABS`
- B. Some lamps are placed on a counter. `P1-LOC`
- C. Some lamps are suspended from a ceiling. ✓
- D. A ceiling is being repaired. `P1-INF`

**Giải thích:** `suspended from` = treo từ. Không người → loại câu `being`.
**Skill:** `be suspended`, `P1-PRG`.

### Tự kiểm tra Bài 3
Đạt khi **≥ 4/5** và gọi đúng tên mã của từng câu sai.

---

# BÀI 4 — NGHE THẬT: ÂM THANH, NỐI ÂM, SỐ VÀ GIỌNG

> Đây là bài quan trọng nhất của chương. Nhiều người sai ở Part 2 không phải vì thiếu từ mà vì **không giải mã được âm**.

## Mục tiêu
- Giải mã nối âm và âm yếu trong câu hỏi thật.
- Nghe được đuôi -ed, -s; số, giờ và giá tiền.
- Quen giọng Anh, Úc, Canada ngoài giọng Mỹ.

## 4.1. Nối âm (linking)

| Viết | Nghe giống như | Ghi chú |
|---|---|---|
| Could you | "couldja" | /d/ + /j/ → /dʒ/ |
| Did you | "didja" | |
| Would you mind | "wouldja mind" | |
| What time is it? | "whattimeizit" | nối liên tục |
| Check it out | "checkitout" | phụ âm cuối nối vào nguyên âm sau |
| Turn it off | "turnitoff" | |
| An apple | "anapple" | |

## 4.2. Âm yếu (weak forms) và các từ chức năng

Từ chức năng thường đọc yếu, nuốt nguyên âm. **Nội dung ý nghĩa nằm ở từ có trọng âm.**

| Từ | Dạng yếu thường gặp |
|---|---|
| can | /kən/ (rất yếu) |
| can't | /kænt/ (rõ, dài hơn trong giọng Mỹ; /kɑːnt/ trong giọng Anh) |
| to | /tə/ |
| for | /fər/ |
| and | /ən/ |
| of | /əv/ hoặc /ə/ |
| have | /əv/ (should've) |
| was | /wəz/ |
| do you | "dyou" hoặc "juh" |

**Cặp nguy hiểm:** `can` vs `can't`. Người học Mỹ thường nghe `can't` nhờ nguyên âm dài hơn và có /t/ cuối nhẹ. Trong câu, hãy nghe **ngữ cảnh** và trọng âm.

## 4.3. Đuôi -ed và -s

Đuôi quyết định thì (quá khứ/hiện tại) và số ít/nhiều. Người học hay "không nghe thấy" nên chọn sai.

| Cặp | Khác biệt |
|---|---|
| work / worked | /wɜːrk/ vs /wɜːrkt/ |
| ask / asked | /æsk/ vs /æskt/ |
| need / needed | /niːd/ vs /niːdɪd/ (thêm âm tiết) |
| order / orders | thêm /z/ cuối |

## 4.4. Số và giờ

- **Cặp -teen / -ty:** 13/30, 14/40, 15/50, 16/60, 17/70, 18/80, 19/90. Trọng âm rơi vào **-teen** (thir-TEEN) và vào âm đầu của **-ty** (THIR-ty).
- **Giờ:** *two fifteen = a quarter past two = two fifteen*; *half past* = :30; *a quarter to* = :45 trước giờ kế.
- **Giá:** *fifteen dollars* vs *fifty dollars*; *two ninety-nine* = 2.99.

## 4.5. Giọng Anh, Úc, Canada (những gì cần quen)

| Từ/hiện tượng | Giọng Mỹ | Giọng khác |
|---|---|---|
| schedule | /ˈskedʒuːl/ | Anh: /ˈʃedjuːl/ |
| can't | /kænt/ | Anh/Úc: /kɑːnt/ |
| water/better | âm /t/ giữa từ có thể thành "d nhẹ" | Anh: /t/ rõ hơn |
| Từ vựng | elevator, apartment, gas, line | lift, flat, petrol, queue |
| Úc | | nguyên âm /eɪ/ có thể nghe gần /aɪ/ ở một số giọng (ví dụ *today*) |

Mục đích không phải bắt chước giọng, mà để **không bị bất ngờ** khi đề đổi giọng.

## 4.6. Drill A — Dictation (nghe và chép)

Quy trình: nghe tối đa **3 lần** ở 1.0x, chép lại, rồi đối chiếu. Mỗi lỗi ghi mã `L-REDUCE`, `L-NUM` hoặc `L-ENDING`.

| # | Audio (đáp án chép) | Chú ý |
|---|---|---|
| D1 | Could you tell me where the personnel office is? | couldja |
| D2 | Did you send the invoice to the supplier? | didja, to |
| D3 | What time does the bank close on Fridays? | whattime, closes |
| D4 | Would you mind forwarding this message? | wouldja |
| D5 | I asked him to check it out yesterday. | asked, checkitout |
| D6 | We need to move the meeting to three thirty. | to, three thirty |
| D7 | The delivery has been put off until the thirteenth. | thirteenth |
| D8 | How much are the monthly passes? Fifty dollars. | much are, fifty |
| D9 | She'll be back at a quarter to nine. | a quarter to |
| D10 | I can't make it to the workshop on Thursday. | can't |

## 4.7. Drill B — Cặp âm gần nhau (minimal pairs)

Audio phát **một từ**, người học chọn từ nghe được. Ghi mã `P1-SND` hoặc `P2-SND` khi sai.

| Nhóm | Cặp |
|---|---|
| Nguyên âm | sheet / seat · live / leave · cheap / chip · full / fool |
| Phụ âm | light / right · pen / pan · work / walk · lunch / launch |
| Tương tự trong bẫy TOEIC | copy / coffee · board / bored · sale / sail · fair / fare |
| Từ đồng âm/gần | weather / whether · accept / except · advice / advise · later / latter |
| Số | 13 / 30 · 14 / 40 · 15 / 50 · 18 / 80 |

## 4.8. Drill C — Số và giờ

Audio phát một cụm, người học chọn con số/giờ đúng:

- *"The workshop starts at four fifteen."* → 4:15 hay 4:50?
- *"It costs thirty dollars."* → $13 hay $30?
- *"We're meeting on the fifteenth."* → 15 hay 50?
- *"A quarter to three."* → 2:45 hay 3:15?

Yêu cầu: **≥ 9/10** ở mỗi bộ drill 10 câu.

## 4.9. Drill D — Shadowing

1. Nghe câu ở 0.85x, đọc to **đồng thời** sau audio khoảng nửa giây.
2. Lặp 3 lần, tăng lên 1.0x ở lần cuối.
3. Chú ý bắt chước **nhịp và nối âm**, không chỉ phát âm từng từ.

### Tự kiểm tra Bài 4
Đạt khi: Dictation ≥ **8/10 câu chép đúng toàn bộ**, minimal pairs ≥ **85%**, drill số ≥ **9/10**. Nếu chưa đạt, quay lại 4.1–4.4 và làm bộ drill mới.

---

# BÀI 5 — PART 2: NHẬN LOẠI CÂU HỎI TRONG 3 TỪ ĐẦU (WH)

## Mục tiêu
- Nghe ra từ để hỏi (**who, what, when, where, why, how, which**) từ 2–3 từ đầu.
- Dự đoán loại thông tin đáp án.
- Loại ngay bẫy lặp từ và bẫy âm.

## 5.1. Bản đồ WH → loại đáp án

| Từ hỏi | Hỏi về | Đáp án thường là |
|---|---|---|
| Who | người | tên, chức vụ, "the new manager", "Ms. Ortega" |
| What | vật/việc | danh từ, mô tả, sự việc |
| When / What time | thời gian | thời điểm, khoảng thời gian, "next week" |
| Where | nơi chốn | địa điểm, "on the shelf", "next to…" |
| Why | lý do | because…, to + V, "the guide is ill" |
| How | cách thức | phương tiện, cách làm |
| How much/many/long/often | số lượng/thời lượng/tần suất | số, "twice a week" |
| Which | lựa chọn | "the one…", "the red folder" |

Lưu ý: **How often** = tần suất (*once a week*); **How long** = bao lâu hoặc từ khi nào (*since 2019*, *two hours*).

## 5.2. Drill "3 từ đầu" (chữa L-FIRST)

Audio chỉ phát **3 từ đầu** của câu hỏi. Người học chọn loại câu hỏi và loại đáp án. Ví dụ: *"Where can I…"* → nơi chốn; *"Who's in charge…"* → người; *"How often do…"* → tần suất.

## 5.3. Cách xử lý ba phản hồi

1. Nghe câu hỏi → **ghi nhớ loại thông tin** (ví dụ: "thời gian").
2. Với mỗi phản hồi: ✓ / ✗ / ?
3. Loại ngay: phản hồi **sai loại thông tin** (**P2-WHQ**), phản hồi bắt đầu bằng **Yes/No** cho câu WH (**P2-YNA**), phản hồi **lặp từ** dùng nghĩa khác (**P2-REP**).

## 5.4. Bài luyện Part 2 (WH)

#### CH02-L05-Q01 · US-F → UK-M · ★1
**Q:** Who's organizing the training session?
- A. At the training center. `P2-WHQ`
- B. Ms. Ortega is. ✓
- C. It was very helpful. `P2-TNS`

**Giải thích:** Who → người.

#### CH02-L05-Q02 · AU-M → US-F · ★1
**Q:** Where can I find the shipping labels?
- A. Next Thursday. `P2-WHQ`
- B. Yes, I labeled them. `P2-YNA`
- C. Check the supply closet. ✓

**Giải thích:** Where → nơi chốn. B còn dính bẫy âm *label/labels*.

#### CH02-L05-Q03 · CA-F → UK-M · ★1
**Q:** What time does the bank close on Fridays?
- A. At five thirty. ✓
- B. It's on Main Street. `P2-WHQ`
- C. I closed the account. `P2-SND`

**Giải thích:** What time → giờ. C bẫy lặp gốc từ *close/closed*.

#### CH02-L05-Q04 · UK-F → US-M · ★2
**Q:** Why was the tour postponed?
- A. Around ten people. `P2-WHQ`
- B. The guide is ill. ✓
- C. To the post office. `P2-SND`

**Giải thích:** Why → lý do. C là bẫy âm *post-poned / post office*.

#### CH02-L05-Q05 · US-M → AU-F · ★2
**Q:** How often do you inspect the equipment?
- A. Yes, I did inspect it. `P2-YNA`
- B. About three hundred dollars. `P2-WHQ`
- C. Once a week. ✓

**Giải thích:** How often → tần suất.

#### CH02-L05-Q06 · CA-M → US-F · ★3
**Q:** Which printer is out of toner?
- A. The one near the entrance. ✓
- B. I'll print it later. `P2-REP`
- C. On Tuesday morning. `P2-WHQ`

**Giải thích:** Which → chọn trong nhóm, đáp bằng "the one…".

### Tự kiểm tra Bài 5
Đạt khi **≥ 5/6**, nhận loại câu hỏi **đúng trong ≤ 3 từ đầu**, và Drill "3 từ đầu" đạt ≥ 90%.

---

# BÀI 6 — PART 2: YES/NO, TAG, PHỦ ĐỊNH VÀ LỰA CHỌN

## Mục tiêu
- Hiểu rằng đáp án Yes/No **không bắt buộc** phải có chữ "Yes/No".
- Xử lý câu hỏi đuôi, phủ định và câu hỏi lựa chọn (A or B).

## 6.1. Câu trả lời gián tiếp cho Yes/No

Người bản ngữ ít khi chỉ nói "Yes". Các phản hồi đúng thường là:
- Xác nhận kèm thông tin: *Yes, I registered last week.*
- Gần như: *Almost—I'm checking the figures.*
- Hoãn: *Let me check my schedule.*
- Điều kiện: *Just finish the report first.*
- Phủ nhận kèm lý do: *No, I have to meet a client that day.*

## 6.2. Câu hỏi đuôi và câu hỏi phủ định

- `You're attending, aren't you?` → trả lời theo **sự thật**: Yes (tôi tham dự) / No (không).
- `Isn't the copier working?` → **Yes = nó đang chạy, No = nó không chạy**. Hãy nghe phần thông tin sau Yes/No để chắc chắn.

## 6.3. Câu hỏi lựa chọn (A or B)

*Would you prefer the window seat or the aisle seat?* → đáp phải **chọn một**, hoặc "either/neither/both". "Yes" hay "No" không chọn được gì (**P2-YNA**).

## 6.4. Bài luyện Part 2

#### CH02-L06-Q01 · US-M → UK-F · ★2
**Q:** Did you finish the sales report?
- A. The sales team is upstairs. `P2-REP`
- B. It's a short report. `P2-REP`
- C. Almost—I'm just checking the figures. ✓

**Giải thích:** Đáp án gián tiếp: "gần xong". A và B lặp từ.

#### CH02-L06-Q02 · UK-F → AU-M · ★2
**Q:** You're attending the seminar, aren't you?
- A. Yes, I registered last week. ✓
- B. It starts at noon. `P2-WHQ`
- C. The seminar was excellent. `P2-TNS`

#### CH02-L06-Q03 · AU-F → CA-M · ★3
**Q:** Isn't the copier working?
- A. I'd like two copies. `P2-SND`
- B. No, a technician is on the way. ✓
- C. In the supply room. `P2-WHQ`

**Giải thích:** Phủ định: "No" = nó không chạy, rồi nêu hành động xử lý.

#### CH02-L06-Q04 · CA-M → US-F · ★2
**Q:** Would you prefer the window seat or the aisle seat?
- A. The aisle, please. ✓
- B. I preferred the movie. `P2-TNS`
- C. Yes, I'd prefer that. `P2-YNA`

**Giải thích:** Câu hỏi chọn → phải chọn một.

#### CH02-L06-Q05 · US-F → AU-M · ★3
**Q:** Can you work this Saturday?
- A. Yes, it was a great weekend. `P2-TNS`
- B. At the Saturday market. `P2-WHQ`
- C. Let me check my schedule. ✓

**Giải thích:** Hoãn trả lời bằng cách xem lịch.

#### CH02-L06-Q06 · UK-M → CA-F · ★3
**Q:** Haven't you submitted the application yet?
- A. On the application form. `P2-REP`
- B. I'm submitting it today. ✓
- C. Yes, a very strong applicant. `P2-REL`

**Giải thích:** Xác nhận "chưa nộp" và cho biết kế hoạch.

### Tự kiểm tra Bài 6
Đạt khi **≥ 5/6** và giải thích được vì sao "Yes/No" không xuất hiện mà đáp án vẫn đúng.

---

# BÀI 7 — PART 2: CÂU HỎI GIÁN TIẾP, YÊU CẦU, ĐỀ NGHỊ, GỢI Ý

## Mục tiêu
- Phản hồi đúng **chức năng giao tiếp** thay vì dịch từng từ.
- Nhận bẫy `Yes` cho `Do you mind…?` và bẫy `Why don't we…?` khác với `Why…?`.

## 7.1. Câu hỏi gián tiếp

*Could you tell me how to get to…? / Do you know when…? / Do you happen to know where…?*
→ Loại thông tin theo **từ hỏi nhúng bên trong** (how, when, where…).

## 7.2. Chức năng và phản hồi tự nhiên

| Câu | Chức năng | Phản hồi thường gặp |
|---|---|---|
| Could you / Can you / Would you…? | nhờ | Sure. / Certainly. / Of course. / Sorry, I can't. |
| Would you mind + V-ing? | nhờ lịch sự | **Not at all.** / No problem. |
| Do you mind if I…? | xin phép | **Go ahead.** / Not at all. / Sorry, I'd rather you didn't. |
| Would you like (me to)…? | đề nghị/mời | I'd love to. / Thanks, that would help. |
| Why don't we / How about / Let's / Shall we…? | gợi ý | Good idea. / Sounds good. / That's a sensible idea. |

## 7.3. Hai bẫy lớn

1. **Do you mind / Would you mind … ?** Trả lời "**Yes**" thường nghĩa là *tôi phiền*. Người ra đề thường tránh dùng, nhưng phản hồi có "Yes, it opens at nine" là bẫy âm/lặp.
2. **Why don't we…?** là gợi ý, **không phải câu hỏi lý do**. Đáp "Because…" là sai (**P2-WHQ**).

## 7.4. Bài luyện Part 2

#### CH02-L07-Q01 · US-M → UK-F · ★1
**Q:** Could you tell me how to get to the conference hall?
- A. Take the elevator to the second floor. ✓
- B. Yes, it was a big conference. `P2-YNA`
- C. About two hundred guests. `P2-WHQ`

#### CH02-L07-Q02 · UK-F → CA-M · ★1
**Q:** Would you like me to carry that for you?
- A. I carried it yesterday. `P2-TNS`
- B. In the trunk of the car. `P2-WHQ`
- C. Thanks, that would help. ✓

#### CH02-L07-Q03 · AU-M → US-F · ★2
**Q:** Why don't we take a short break?
- A. The break was only ten minutes. `P2-TNS`
- B. Good idea—I need some coffee. ✓
- C. Because it's far. `P2-WHQ`

**Giải thích:** `Why don't we` = gợi ý, đáp bằng đồng ý.

#### CH02-L07-Q04 · CA-F → UK-M · ★3
**Q:** Do you mind if I open the window?
- A. Yes, it opens at nine. `P2-SND`
- B. At the front of the room. `P2-WHQ`
- C. Go ahead—it's warm in here. ✓

**Giải thích:** `Do you mind if I…` → "Go ahead" = tôi không phiền.

#### CH02-L07-Q05 · US-F → AU-M · ★2
**Q:** Could I borrow your stapler for a moment?
- A. Sure, it's on my desk. ✓
- B. I borrowed it last month. `P2-TNS`
- C. It's a stable job. `P2-SND`

#### CH02-L07-Q06 · UK-M → US-F · ★3
**Q:** Shall we go over the budget figures together?
- A. The figures are in the folder. `P2-REL`
- B. Yes, let's do that after lunch. ✓
- C. The budget was approved. `P2-TNS`

### Tự kiểm tra Bài 7
Đạt khi **≥ 5/6** và giải thích được mỗi câu đáp **chức năng giao tiếp** nào.

---

# BÀI 8 — PART 2: CÂU TRẦN THUẬT VÀ CÂU TRẢ LỜI GIÁN TIẾP

## Mục tiêu
- Phản hồi đúng với một câu **không phải câu hỏi**.
- Nhận ra câu trả lời "không biết", "hỏi người khác", "xem đã".

## 8.1. Câu trần thuật nêu vấn đề

Khi người nói đưa ra một **vấn đề** (máy hỏng, hết giấy, thiếu hàng), phản hồi tốt thường là **giải pháp** hoặc **câu hỏi làm rõ**:

- *The projector isn't working again.* → *I'll ask IT to take a look.*
- *We're almost out of coffee.* → *I'll pick some up on my way in.*
- *I can't find my access card.* → *Did you check the lost-and-found box?*

Phản hồi sai thường: lặp lại từ khóa, mô tả vật, hoặc nói thông tin không liên quan.

## 8.2. Câu trả lời gián tiếp phổ biến

| Kiểu | Ví dụ |
|---|---|
| Không biết | *I'm not sure. / I have no idea.* |
| Chuyển hướng | *Ask the receptionist. / You'd have to check with HR.* |
| Hoãn | *Let me find out. / I'll get back to you.* |
| Thông tin mới | *It was extended until Friday.* |
| Phản câu hỏi | *Did you check the lost-and-found box?* |

Câu trả lời gián tiếp thường là đáp án đúng ở các câu **khó**. Đừng loại chỉ vì không khớp từ.

## 8.3. Bài luyện Part 2

#### CH02-L08-Q01 · US-M → UK-F · ★2
**Q:** I can't find my access card.
- A. It's accessible to everyone. `P2-SND`
- B. Did you check the lost-and-found box? ✓
- C. It's due on Friday. `P2-REL`

#### CH02-L08-Q02 · UK-F → AU-M · ★1
**Q:** The projector isn't working again.
- A. I'll ask IT to take a look. ✓
- B. Yes, a good project. `P2-SND`
- C. The movie was long. `P2-REL`

#### CH02-L08-Q03 · AU-F → CA-M · ★2
**Q:** We're almost out of coffee.
- A. I'm out of town. `P2-REP`
- B. Yes, I drank coffee. `P2-TNS`
- C. I'll pick some up on my way in. ✓

#### CH02-L08-Q04 · CA-M → US-F · ★3
**Q:** I thought the deadline was tomorrow.
- A. In the Dallas office. `P2-WHQ`
- B. It was extended until Friday. ✓
- C. I'll be on vacation tomorrow. `P2-REP`

**Giải thích:** Thông tin mới điều chỉnh niềm tin của người nói.

#### CH02-L08-Q05 · US-F → UK-M · ★3
**Q:** Where did Ms. Park go?
- A. At two o'clock. `P2-WHQ`
- B. She parked in the garage. `P2-SND`
- C. Ask the receptionist—she might know. ✓

**Giải thích:** Câu trả lời chuyển hướng hợp lý.

#### CH02-L08-Q06 · UK-M → AU-F · ★2
**Q:** How was the client meeting?
- A. It went better than expected. ✓
- B. At the main office. `P2-WHQ`
- C. Next Monday at ten. `P2-TNS`

### Tự kiểm tra Bài 8
Đạt khi **≥ 5/6** và nêu được **kiểu phản hồi** (giải pháp, chuyển hướng, thông tin mới…).

---

# BÀI 9 — PART 2: PARAPHRASE VÀ BẢN ĐỒ BẪY TỔNG HỢP

## Mục tiêu
- Nhận đáp án đúng khi **không lặp từ**, dùng từ đồng nghĩa.
- Dùng quy trình loại trừ có hệ thống.

## 9.1. Bảng paraphrase thường gặp

| Từ trong câu hỏi | Có thể xuất hiện trong đáp án |
|---|---|
| purchase | buy, bought |
| postpone | put off, push back |
| available | free, open |
| begin | start |
| complete | finish |
| cost | be priced at, come to |
| reserve | book |
| cancel | call off |
| approximately | about, around |
| in the building | in, out (phủ định gián tiếp) |

## 9.2. Quy tắc nghịch lý

Trong Part 2, **đáp án đúng thường ít lặp từ khóa của câu hỏi**; đáp án lặp từ hay là bẫy. Nhưng đừng loại máy móc: hãy kiểm tra **chức năng**.

## 9.3. Quy trình loại trừ 4 bước

1. **Loại thông tin:** câu hỏi cần gì (người, nơi, giờ…)?
2. Loại phản hồi **sai loại** (`P2-WHQ`, `P2-YNA`).
3. Loại phản hồi **lặp từ** hoặc **gần âm** (`P2-REP`, `P2-SND`).
4. Trong phần còn lại, chọn phản hồi **thực sự giải quyết** câu hỏi, kể cả khi nó gián tiếp.

## 9.4. Bài luyện Part 2

#### CH02-L09-Q01 · US-M → UK-F · ★1
**Q:** Have you purchased the tickets?
- A. The tickets are expensive. `P2-REP`
- B. She's a ticket agent. `P2-REL`
- C. Yes, I bought them online. ✓

**Giải thích:** purchase → bought.

#### CH02-L09-Q02 · UK-F → AU-M · ★3
**Q:** Is the manager in the building?
- A. It's a tall building. `P2-REP`
- B. She's out until two. ✓
- C. At the front desk. `P2-WHQ`

**Giải thích:** "out" là phủ định gián tiếp.

#### CH02-L09-Q03 · AU-M → CA-F · ★2
**Q:** Can you reserve a table for six?
- A. I'll book one for seven o'clock. ✓
- B. The reserve tank is full. `P2-SND`
- C. Six people attended. `P2-TNS`

**Giải thích:** reserve → book.

#### CH02-L09-Q04 · CA-F → US-M · ★2
**Q:** Will the renovation be completed by June?
- A. In the lobby area. `P2-WHQ`
- B. I renovated the kitchen. `P2-TNS`
- C. They should finish in May. ✓

**Giải thích:** completed → finish; "in May" trước June.

#### CH02-L09-Q05 · US-F → UK-M · ★2
**Q:** How much will the repairs cost?
- A. The repair shop closes at six. `P2-REP`
- B. It'll come to about four hundred dollars. ✓
- C. By next Friday. `P2-WHQ`

**Giải thích:** cost → come to.

#### CH02-L09-Q06 · UK-M → AU-F · ★3
**Q:** Is Mr. Kim still working here?
- A. No, he left the company last spring. ✓
- B. Yes, I'll work late. `P2-REP`
- C. At the Kim brothers' shop. `P2-REL`

### Tự kiểm tra Bài 9
Đạt khi **≥ 5/6** và gọi đúng tên bẫy của ít nhất 4 phản hồi sai.

---

# KIỂM TRA CUỐI CHƯƠNG 2

**Số câu:** 25 (Part 1: 6, Part 2: 19) · **Thời gian:** 18–22 phút
**Điều kiện:** 1.0x, nghe một lần, không transcript, không xem giải thích trước khi nộp.
**Đạt chương:** ≥ **20/25** và Part 1 ≥ 5/6.

## Part 1

#### CH02-FINAL-Q01 · US-M
**Ảnh:** Một nhân viên chỉnh lại màn hình trên bàn làm việc.
- A. A man is carrying a monitor up some stairs. `P1-ACT`
- B. A monitor is being delivered to a customer. `P1-INF`
- C. A man is turning off the lights. `P1-ACT`
- D. A man is adjusting a monitor. ✓

#### CH02-FINAL-Q02 · UK-F
**Ảnh:** Một hàng chậu cây dọc lối đi cạnh tòa nhà kính; không có người.
- A. Some plants are lined up along a walkway. ✓
- B. Some plants are being watered by a gardener. `P1-ABS`
- C. A building is being constructed. `P1-INF`
- D. Some plants are hanging over a bridge. `P1-LOC`

#### CH02-FINAL-Q03 · AU-M
**Ảnh:** Hai người ngồi bên bàn xem biểu đồ trên máy tính bảng; một người chỉ vào màn hình.
- A. They are setting up a projector. `P1-ACT`
- B. They are signing a document. `P1-ABS`
- C. One of them is pointing at a tablet. ✓
- D. They are shaking hands. `P1-ACT`

#### CH02-FINAL-Q04 · CA-F
**Ảnh:** Một người phụ nữ **đang mặc** áo khoác, cầm ô, đứng cạnh giá treo áo.
- A. A woman is hanging up her coat. `P1-PRG`
- B. A woman is holding an umbrella. ✓
- C. A woman is opening a door. `P1-ACT`
- D. A woman is buying a coat. `P1-INF`

#### CH02-FINAL-Q05 · US-F
**Ảnh:** Hộp chất cạnh bến bốc hàng; một xe nâng đỗ bên cạnh; không có người.
- A. A forklift is lifting a box. `P1-ABS`
- B. A forklift is parked next to some boxes. ✓
- C. Workers are unloading a truck. `P1-ABS`
- D. Some boxes are being wrapped. `P1-PRG`

#### CH02-FINAL-Q06 · UK-M
**Ảnh:** Một người đàn ông rút một quyển sách từ kệ cao trong thư viện; không có thang.
- A. A man is taking a book from a shelf. ✓
- B. A man is returning a book at the counter. `P1-LOC`
- C. A man is climbing a ladder. `P1-ABS`
- D. Some shelves are being moved. `P1-PRG`

## Part 2

#### CH02-FINAL-Q07 · US-F → UK-M
**Q:** Who left this package on my desk?
- A. On the second shelf. `P2-WHQ`
- B. I think it was the courier. ✓
- C. The desk is new. `P2-REP`

#### CH02-FINAL-Q08 · AU-M → US-F
**Q:** When is the next shuttle to the airport?
- A. Terminal two. `P2-WHQ`
- B. Yes, I'll take it. `P2-YNA`
- C. In about ten minutes. ✓

#### CH02-FINAL-Q09 · UK-F → CA-M
**Q:** Where should I put the new brochures?
- A. On the table by the entrance. ✓
- B. They're printed in color. `P2-REL`
- C. Brochure design is Tom's job. `P2-REL`

#### CH02-FINAL-Q10 · CA-F → US-M
**Q:** Do you want the report printed or sent by e-mail?
- A. It was printed yesterday. `P2-TNS`
- B. No, I don't. `P2-YNA`
- C. E-mail is fine. ✓

#### CH02-FINAL-Q11 · US-M → AU-F
**Q:** Aren't you going to the trade show?
- A. I showed him the way. `P2-SND`
- B. No, I have to meet a client that day. ✓
- C. Next to the convention center. `P2-WHQ`

#### CH02-FINAL-Q12 · UK-M → US-F
**Q:** Could you help me move these chairs?
- A. Sure, which room? ✓
- B. They're comfortable chairs. `P2-REP`
- C. Yes, I moved last year. `P2-TNS`

#### CH02-FINAL-Q13 · AU-F → CA-M
**Q:** Why don't you try the new Italian restaurant?
- A. Because I was late. `P2-WHQ`
- B. I'm trying a new job. `P2-REP`
- C. I will—do you have its address? ✓

#### CH02-FINAL-Q14 · US-F → UK-M
**Q:** The elevator is out of service.
- A. Then let's use the stairs. ✓
- B. I served lunch. `P2-SND`
- C. Yes, it's the third floor. `P2-REL`

#### CH02-FINAL-Q15 · CA-M → AU-F
**Q:** How long have you worked here?
- A. About five kilometers. `P2-WHQ`
- B. Since 2019. ✓
- C. By bus, usually. `P2-WHQ`

#### CH02-FINAL-Q16 · US-M → UK-F
**Q:** Is it all right if I leave early today?
- A. Yes, it's right here. `P2-SND`
- B. At about five. `P2-WHQ`
- C. Just finish the report first. ✓

#### CH02-FINAL-Q17 · UK-F → US-M
**Q:** What did the client think of the proposal?
- A. She asked for a few changes. ✓
- B. In the conference room. `P2-WHQ`
- C. I think so too. `P2-REL`

#### CH02-FINAL-Q18 · AU-M → CA-F
**Q:** Would you mind turning down the music?
- A. It's playing at nine. `P2-WHQ`
- B. Sorry, I'll turn it down. ✓
- C. The turn is on the left. `P2-SND`

#### CH02-FINAL-Q19 · CA-F → US-F
**Q:** Who's going to present the quarterly figures?
- A. In the main hall. `P2-WHQ`
- B. Quarter past four. `P2-SND`
- C. Ms. Alvarez volunteered. ✓

#### CH02-FINAL-Q20 · US-F → UK-M
**Q:** Do you know how much the conference registration is?
- A. It's one hundred fifty dollars. ✓
- B. In the registry office. `P2-SND`
- C. The conference was long. `P2-TNS`

#### CH02-FINAL-Q21 · UK-M → AU-F
**Q:** We should hire another designer.
- A. It's a nice design. `P2-REP`
- B. Let's check whether the budget allows it. ✓
- C. I hired him last month. `P2-TNS`

#### CH02-FINAL-Q22 · AU-F → US-M
**Q:** Which seat is yours?
- A. At the front desk. `P2-WHQ`
- B. Yes, I sat there. `P2-YNA`
- C. The one by the window. ✓

#### CH02-FINAL-Q23 · US-M → CA-F
**Q:** Has the new employee started yet?
- A. She begins on Monday. ✓
- B. It's a new office. `P2-REP`
- C. About fifty employees. `P2-WHQ`

#### CH02-FINAL-Q24 · CA-M → UK-F
**Q:** Where's the nearest copy center?
- A. I'd like some coffee. `P2-SND`
- B. There's one around the corner. ✓
- C. Yes, I'll copy them. `P2-YNA`

#### CH02-FINAL-Q25 · UK-F → AU-M
**Q:** Why is the lobby so crowded?
- A. It's on the first floor. `P2-WHQ`
- B. I lobbied for it. `P2-SND`
- C. There's a job fair this morning. ✓

## Đáp án gốc (CHỈ dành cho người soạn nội dung)

| Câu | Đ.án | Kỹ năng | Câu | Đ.án | Kỹ năng |
|---:|:--:|---|---:|:--:|---|
| 1 | D | Part 1 action | 14 | A | statement → giải pháp |
| 2 | A | vị trí, không người | 15 | B | How long / since |
| 3 | C | pointing | 16 | C | xin phép, trả lời điều kiện |
| 4 | B | wearing vs putting on | 17 | A | What + phản ứng |
| 5 | B | vật, không người | 18 | B | Would you mind |
| 6 | A | action | 19 | C | Who |
| 7 | B | Who | 20 | A | indirect + giá |
| 8 | C | When | 21 | B | statement → làm rõ |
| 9 | A | Where | 22 | C | Which |
| 10 | C | chọn A hay B | 23 | A | paraphrase started/begins |
| 11 | B | phủ định + lý do | 24 | B | Where + SND copy/coffee |
| 12 | A | request | 25 | C | Why |
| 13 | C | suggestion | | | |

> Bảng trên chỉ là đáp án gốc. **Runtime phải xáo vị trí đáp án**, không được để vị trí đúng cố định.

## Chẩn đoán sau Final Test

App tổng hợp theo `distractor_code` và mã lỗi nghe:

| Kết quả | Hành động |
|---|---|
| Sai ≥ 2 cùng một mã bẫy | Mở bài sửa lỗi tương ứng (mục 3.1–3.2) |
| Sai nhiều ở các câu có nối âm/số | Mở drill Bài 4 |
| Sai ở Part 2 cuối bài (nhiều lựa chọn tạo nhầm trí nhớ) | Luyện L-MEMORY: nhắc lại câu hỏi trong đầu trước khi nghe đáp án A |
| Đạt ≥ 20/25 và Part 1 ≥ 5/6 | Đánh dấu `CH02_PASS` |

---

## Từ vựng Chương 2

> Từ vựng TOEIC nền tảng đã có sẵn trong ứng dụng. Danh sách này chỉ liệt kê các cụm xuất hiện trong chương, để đối chiếu.

examine/inspect · operate · load/unload · arrange · point at · hand · shake hands · beside · between · underneath · along · lean against · be stacked/stored/suspended · be positioned · postpone/put off · call off/cancel · available/free · reserve/book · complete/finish · be priced at/come to · supervisor · supplier · quotation · revised · registration · quarterly figures · access card · lost-and-found · shuttle · trade show · job fair.

## Điều kiện hoàn thành Chương 2

1. Hoàn thành 9 bài và đạt ngưỡng từng bài.
2. Bài 4 đạt đủ 3 chỉ tiêu (dictation, minimal pairs, số).
3. Final Test mới ở 1.0x, không transcript, đạt ≥ 20/25 và Part 1 ≥ 5/6.
4. Mọi câu sai đã vào **Mistake Book**; mỗi mã lỗi có ít nhất 1 vòng sửa lỗi hoàn tất.
5. Khi đạt, app đánh dấu `CH02_PASS`; Chương 3 chưa mở cho đến khi có nội dung và registry được cập nhật.
