# CONTENT REGISTRY — QUẢN LÝ NỘI DUNG TOEIC LISTENING 300

**Phiên bản registry:** 2.3  
**Phiên bản Spec (`specVersion`):** 2.3  
**Phiên bản Nội dung (`contentVersion`):** 1.0.0  
**Cập nhật:** 23-11-2026  
**Mục đích:** theo dõi rõ nội dung đã biên soạn, nội dung còn thiếu, trạng thái audio và trạng thái triển khai trên web.  
**Quy tắc:** không đánh dấu “Hoàn thành” chỉ vì đã có ý tưởng/chủ đề; phải có giáo trình chi tiết, câu hỏi, đáp án, giải thích và được kiểm tra.

---

## 1. Tổng quan trạng thái

| Mã | Nội dung | Giáo trình MD | Câu hỏi + đáp án + giải thích | Audio script | Audio MP3 | Đã tích hợp web | Trạng thái |
|---|---|---:|---:|---:|---:|---:|---|
| WEB-SPEC | Spec website GitHub Pages miễn phí | Có | N/A | Có, đã quy định | Chưa chạy | Chưa | Đã cập nhật v2.3 |
| CH01 | Nền tảng nghe | Có | Có | Có, nằm trong nội dung | Chưa sinh | Chưa | Nội dung đã biên soạn (45 câu) |
| CH02 | Part 1 + Part 2 mở rộng | Có | Có | Có, nằm trong nội dung | Chưa sinh | Chưa | Nội dung đã biên soạn (41 câu, 18 ảnh SVG) |
| CH03 | Part 3 cơ bản (hội thoại nam/nữ) | Có | Có | Có, nằm trong nội dung | Chưa sinh | Chưa | Nội dung đã biên soạn (14 hội thoại, 42 câu) |
| CH04 | Part 3 nâng cao | Chưa | Chưa | Chưa | Chưa | Chưa | Chưa tạo |
| CH05 | Part 4 cơ bản | Chưa | Chưa | Chưa | Chưa | Chưa | Chưa tạo |
| CH06 | Part 4 nâng cao | Chưa | Chưa | Chưa | Chưa | Chưa | Chưa tạo |
| CH07 | Ôn tập Part 1–4 | Chưa | Chưa | Chưa | Chưa | Chưa | Chưa tạo |
| MOCK | Thi thử Listening 100 câu | Chưa | Chưa | Chưa | Chưa | Chưa | Chưa tạo |

**Lưu ý quan trọng:** Hiện tại đã biên soạn xong nội dung Markdown cho cả 3 chương: Chương 1, Chương 2 và Chương 3 (`CHAPTER_01_CONTENT.md`, `CHAPTER_02_CONTENT.md`, `CHAPTER_03_CONTENT.md`). Quy chuẩn mã hóa ID nhóm hội thoại Part 3 được thống nhất là `CH03-Lxx-Gxx`.

---

## 2. Danh mục file đã tạo

| File | Vai trò | Trạng thái |
|---|---|---|
| `SPEC_WEB_APP.md` | Đặc tả công nghệ, giao diện, Part 3/4 groups, voice nam/nữ, TTS local CBR, GitHub Pages, optionsVisibleBeforeAnswer | Đã cập nhật v2.3 |
| `PROGRESS_STORAGE_SPEC.md` | Lưu lịch sử, groupId, xáo đáp án, cơ chế khắc phục lỗi theo `skillGroup`, sao lưu/gộp | Đã cập nhật v1.2 |
| `CHAPTER_01_CONTENT.md` | Toàn bộ nội dung học Chương 1, bài luyện, final test, đáp án (45 câu) | Đã tạo |
| `CHAPTER_02_CONTENT.md` | Toàn bộ nội dung học Chương 2, bài luyện, final test, đáp án (41 câu, 18 ảnh SVG) | Đã tạo |
| `CHAPTER_03_CONTENT.md` | Toàn bộ nội dung học Chương 3 Part 3, 14 hội thoại, final test, đáp án (42 câu) | Đã tạo |
| `CONTENT_REGISTRY.md` | Bảng quản lý nội dung đã/chưa tạo | Đã cập nhật v2.3 |
| `voices.example.json` | Mẫu cấu hình một voice nữ + một voice nam có kiểm tra license | Đã tạo |

---

## 3. Chi tiết chương đã biên soạn

### CH01 — Nền tảng nghe

| Mã bài | Tên bài | Số câu luyện | Mục tiêu | Pass Rule | Tình trạng |
|---|---|---:|---|---|---|
| CH01-L01 | Nghe từ mang thông tin chính | 4 | Content words, ý chính, thời gian/địa điểm | 3/4 (75%) | Đã tạo |
| CH01-L02 | Âm cuối và dạng rút gọn | 4 | -s/-es, -ed, contractions | 3/4 (75%) | Đã tạo |
| CH01-L03 | Số, giờ, ngày tháng và giá tiền | 5 | Number/time recognition | 4/5 (80%) | Đã tạo |
| CH01-L04 | Nhận diện từ để hỏi | 5 | Who/Where/When/Why/How | 4/5 (80%) | Đã tạo |
| CH01-L05 | Part 2 cơ bản | 12 | Response matching, distractors | 10/12 (83.3%) | Đã tạo |
| CH01-FINAL | Kiểm tra cuối chương | 15 | Tổng hợp, câu mới | 12/15 (80%) | Đã tạo |

**Tổng câu nội dung Chương 1:** 45 câu (30 câu luyện + 15 câu final test). CH01-L01 đến L03 có câu hỏi tiếng Việt, hiển thị lựa chọn trên màn hình (`optionsVisibleBeforeAnswer: true`).

### CH02 — Part 1 và Part 2 mở rộng

| Mã bài | Tên bài | Số câu luyện | Mục tiêu | Pass Rule | Tình trạng |
|---|---|---:|---|---|---|
| CH02-L01 | Part 1: người và hành động | 4 | Action verbs, present continuous | 3/4 (75%) | Đã tạo (4 ảnh SVG) |
| CH02-L02 | Part 1: vị trí và đồ vật | 4 | Prepositions, spatial relations | 3/4 (75%) | Đã tạo (4 ảnh SVG) |
| CH02-L03 | Part 1: bị động và bẫy suy diễn | 4 | Passive voice, supported detail | 3/4 (75%) | Đã tạo (4 ảnh SVG) |
| CH02-L04 | Part 2: câu hỏi gián tiếp và giao tiếp | 6 | Indirect questions, requests, offers | 5/6 (83.3%) | Đã tạo |
| CH02-L05 | Part 2: paraphrase và phản hồi tự nhiên | 8 | Paraphrase, statement response | 6/8 (75%) | Đã tạo |
| CH02-FINAL | Kiểm tra cuối chương | 15 | Tổng hợp Part 1 (6 câu, 6 ảnh SVG) + Part 2 (9 câu) | 12/15 (80%) | Đã tạo |

**Tổng câu nội dung Chương 2:** 41 câu (26 câu luyện + 15 câu final test). Tổng cộng **18 ảnh SVG** cho Part 1. Lựa chọn văn bản Part 1 & 2 bị ẩn trước khi trả lời (`optionsVisibleBeforeAnswer: false`).

### CH03 — Part 3 cơ bản: hội thoại hai người

| Mã bài | Tên bài | Số hội thoại (Group) | Số câu | Mục tiêu | Pass Rule | Tình trạng |
|---|---|---:|---:|---|---|---|
| CH03-L01 | Cấu trúc Part 3 & nghe mục đích hội thoại | 2 groups (G01, G02) | 6 | Purpose, topic, next action | 5/6 (83.3%) | Đã tạo |
| CH03-L02 | Địa điểm, nghề nghiệp, quan hệ người nói | 2 groups (G01, G02) | 6 | Place, occupation, inference | 5/6 (83.3%) | Đã tạo |
| CH03-L03 | Chi tiết: thời gian, số, đồ vật | 2 groups (G01, G02) | 6 | Detail, time, number | 5/6 (83.3%) | Đã tạo |
| CH03-L04 | Vấn đề, yêu cầu, đề nghị, việc tiếp theo | 2 groups (G01, G02) | 6 | Problem, request, offer | 5/6 (83.3%) | Đã tạo |
| CH03-L05 | Paraphrase và bẫy trong Part 3 | 2 groups (G01, G02) | 6 | Paraphrase, speaker trap | 5/6 (83.3%) | Đã tạo |
| CH03-FINAL | Kiểm tra cuối chương | 4 groups (G01..G04) | 12 | Tổng hợp Part 3 (4 hội thoại mới) | 10/12 (83.3%) | Đã tạo |

**Tổng câu nội dung Chương 3:** 14 hội thoại, 42 câu hỏi (10 hội thoại luyện = 30 câu + 4 hội thoại final = 12 câu). Thống nhất định dạng mã nhóm `CH03-Lxx-Gxx`.

---

## 4. Hạng mục triển khai

| Hạng mục | Việc cần làm | Trạng thái |
|---|---|---|
| JSON Chương 1 | Chuyển Markdown thành `data/chapters/chapter-01.json` | Cần tạo |
| JSON Chương 2 | Chuyển Markdown thành `data/chapters/chapter-02.json` | Cần tạo |
| JSON Chương 3 | Chuyển Markdown thành `data/chapters/chapter-03.json` | Cần tạo |
| Course JSON | Tạo `course.json`, hỗ trợ CH01, CH02, CH03 | Cần tạo |
| Audio manifest | Manifest phân đoạn cho CH01, CH02, CH03 (CBR MP3) | Cần tạo |
| Scripts TTS | `scripts/voice_audition.py` & `scripts/generate_audio.py` (kiểm tra license, CBR encoding) | Cần tạo |
| Ảnh Part 1 Chương 2 | 18 ảnh SVG vector cục bộ, tối ưu | Cần tạo |
| Validator | `scripts/check_content.py` | Cần tạo |
| Web app | HTML5/CSS3/Vanilla JS (ES6+), LocalStorage, Mistake Book with `skillGroup` | Cần tạo |
| Kiểm thử lưu trữ | `tests/progress-test.html` | Cần tạo |

---

## 5. Lộ trình nội dung

| Thứ tự | Chương | Nội dung | Trạng thái |
|---:|---|---|---|
| 1 | CH01 | Nền tảng nghe | Đã tạo nội dung |
| 2 | CH02 | Part 1 + Part 2 mở rộng | Đã tạo nội dung |
| 3 | CH03 | Part 3 cơ bản: hội thoại 2 người | Đã tạo nội dung |
| 4 | CH04 | Part 3 nâng cao: hội thoại 3 người, bảng biểu | Sau CH03 |
| 5 | CH05 | Part 4 cơ bản: thông báo, tin nhắn thoại | Sau CH04 |
| 6 | CH06 | Part 4 nâng cao: bài nói công cộng, quảng cáo | Sau CH05 |
| 7 | CH07 | Ôn tập tổng hợp Listening Part 1–4 | Sau CH06 |
| 8 | MOCK | Thi thử 100 câu theo chuẩn TOEIC Listening | Sau CH07 |

---

## 6. Lịch sử phiên bản

| Phiên bản | Ngày | Thay đổi |
|---|---|---|
| 2.0 | 23-11-2026 | Tách spec web và giáo trình; tạo nội dung CH01 và CH02; tạo registry độc lập. |
| 2.1 | 23-11-2026 | Spec theo nội dung tệp người học cung cấp. |
| 2.2 | 23-11-2026 | Bổ sung nhóm Part 3/4, hai voice nam/nữ local, voice audition, một MP3/hội thoại, timestamp nghe lại từng lượt, groupId/optionOrder và xáo đáp án. |
| 2.3 | 23-11-2026 | Tích hợp toàn diện CH03 (14 hội thoại, 42 câu, mã nhóm CH03-Lxx-Gxx). Tách rõ `specVersion` (2.3) và `contentVersion` (1.0.0). Bổ sung `passRule` tường minh từng bài để giải quyết xung đột 80% (75% cho bài 4 câu và 8 câu). Bổ sung `skillGroup` cho cơ chế chữa lỗi dứt điểm. Chuẩn hóa `optionsVisibleBeforeAnswer: false` cho Part 1/2. Bắt buộc MP3 mã hóa CBR + bù offset encoder delay cho timestamp chính xác dưới 150 ms. Quy định kiểm tra license giọng đọc phát hành lại audio public repo. |
