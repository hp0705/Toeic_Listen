# SPEC WEB APP — TOEIC LISTENING 300 (GITHUB PAGES / FREE)

**Phiên bản Spec (`specVersion`):** 2.3  
**Phiên bản Nội dung chuẩn (`contentVersion`):** 1.0.0  
**Ngày cập nhật:** 23-11-2026  
**Mục tiêu:** Web app luyện TOEIC Listening hướng tới mục tiêu 300/495  
**Môi trường:** Trình duyệt trên điện thoại và máy tính, triển khai bằng GitHub Pages (phát triển và kiểm thử local)  
**Quản lý source:** Git + GitHub (Repo public: `https://github.com/hp0705/Toeic_Listen.git`)  
**Nguyên tắc:** Miễn phí, tĩnh 100%, không cần AI runtime, không cần tài khoản, không backend, không dịch vụ trả phí.  
**Tài liệu đi kèm bắt buộc:**
- `PROGRESS_STORAGE_SPEC.md` (v1.2) — đặc tả chi tiết việc lưu lịch sử học, sao lưu, gộp tiến độ và giải quyết lỗi theo `skillGroup`.
- `CONTENT_REGISTRY.md` (v2.3) — bảng quản lý nội dung các chương.
- `CHAPTER_01_CONTENT.md`, `CHAPTER_02_CONTENT.md`, `CHAPTER_03_CONTENT.md` — toàn bộ giáo trình 3 chương đã biên soạn hoàn chỉnh.

---

## 1. Mục tiêu và phạm vi

Xây một web app học TOEIC Listening phục vụ người học tự luyện từ mức cơ bản đến 300/495. Toàn bộ mã nguồn và dữ liệu chạy dưới dạng static site trên GitHub Pages (`https://hp0705.github.io/Toeic_Listen/`). Khi phát triển chạy local bằng `python -m http.server 8000`.

Lịch sử học được lưu **trong trình duyệt của từng thiết bị** (LocalStorage), có công cụ sao lưu/khôi phục file JSON và tính năng gộp tiến độ giữa nhiều thiết bị (xem `PROGRESS_STORAGE_SPEC.md`).

### Các tính năng cốt lõi của App:
1. Hiển thị chương, bài học, khối kiến thức giải thích tiếng Việt, ví dụ và bài tập.
2. Phát audio MP3 mã hóa chuẩn CBR với player hỗ trợ tốc độ 1.0x và 0.85x.
3. Chấm đáp án dựa trên answer key trong dữ liệu cục bộ; hỗ trợ xáo thứ tự lựa chọn khi làm bài để chống học vẹt.
4. Kiểm soát việc hiển thị lựa chọn (`optionsVisibleBeforeAnswer`):
   - Với Part 1 & Part 2: Chỉ hiển thị nút chọn A–D, ẩn văn bản đáp án trước khi trả lời để người học buộc phải luyện nghe thay vì đọc trước.
   - Với Foundation (CH01-L01..L03) và Part 3: Hiển thị câu hỏi tiếng Việt/tiếng Anh và các lựa chọn trên màn hình để đọc trước.
5. Giải thích chi tiết vì sao đáp án đúng và phân tích cặn kẽ từng phương án sai (distractors).
6. Sổ lỗi (Mistake Book) tự động ghi nhận câu sai, gắn `skillTags` và `skillGroup`.
7. Cơ chế khắc phục lỗi dứt điểm: Người học xóa được lỗi khi làm đúng một câu hỏi mới ở 1.0x (không xem transcript trước) có cùng `skillTag` HOẶC cùng `skillGroup` (với Part 3 phải khác `groupId`).
8. Theo dõi tiến độ từng bài với `passRule` tường minh (hỗ trợ các bài 4 câu đạt 3/4 = 75%, bài 8 câu đạt 6/8 = 75%, các bài khác 80%).
9. Mở khóa tuần tự: CH01 mở sẵn; CH02 mở khi đạt >= 80% CH01-FINAL; CH03 mở khi đạt >= 80% CH02-FINAL.
10. Hệ thống sao lưu an toàn: Xuất file JSON (kèm `coachSummary`), Nhập Gộp (Merge) hoặc Nhập Thay thế (Replace) kèm tính năng Hoàn tác (Undo).

### Giới hạn công nghệ (Strict Constraints):
- Không gọi bất kỳ AI API nào (Gemini, OpenAI, Claude...) từ trình duyệt. Không chứa API key trong source code.
- Không dùng cloud TTS tốn phí. Audio được tạo trước offline trên máy bằng TTS local.
- Không cần tài khoản người dùng, không server database, không Firebase/Supabase.
- Không dùng React, Vue, Next.js, TypeScript, Vite hay Node.js runtime. Ứng dụng là HTML5, CSS3 và Vanilla JavaScript (ES6+ Modules) thuần túy.

---

## 2. Công nghệ được phép sử dụng

| Thành phần | Công nghệ | Bắt buộc? | Ghi chú |
|---|---|---:|---|
| Giao diện | HTML5 + CSS3 | Có | Thiết kế mobile-first, responsive mượt mà |
| Logic | JavaScript thuần (ES6+) | Có | Tách module rõ ràng, không cần build tool |
| Nội dung | JSON | Có | Tách bạch hoàn toàn nội dung khỏi mã nguồn |
| Lưu tiến độ | LocalStorage | Có | Schema v2, có bọc an toàn chống tràn bộ nhớ |
| Âm thanh | MP3 Mono CBR | Có | CBR bitrate ổn định (64–128 kbps), bù encoder delay |
| Tạo giọng đọc | Python + Piper / TTS | Có | Kiểm tra license phát hành public |
| Máy chủ dev | Python `http.server` | Có | `python -m http.server 8000` |
| Triển khai | GitHub Pages | Có | Phục vụ từ branch `main`, thư mục root `/` |

---

## 3. Cấu trúc thư mục source bắt buộc

```text
Toeic_Listen/
│
├── index.html
├── .nojekyll                      # bắt buộc cho GitHub Pages
├── .gitignore
├── README.md
├── SPEC_WEB_APP.md
├── PROGRESS_STORAGE_SPEC.md
├── CONTENT_REGISTRY.md
│
├── css/
│   └── app.css
│
├── js/
│   ├── app.js
│   ├── data-loader.js
│   ├── router.js
│   ├── lesson-view.js
│   ├── quiz.js
│   ├── audio-player.js
│   ├── storage.js          # quản lý LocalStorage (theo PROGRESS_STORAGE_SPEC)
│   ├── progress.js         # rebuildDerived, mở khóa chương, tính passRule
│   ├── mistake-book.js     # sổ lỗi và xác nhận khắc phục theo skillGroup
│   ├── backup.js           # export / import / merge / coachSummary
│   └── history-view.js     # trang Lịch sử & Sao lưu
│
├── data/
│   ├── course.json
│   ├── chapters/
│   │   ├── chapter-01.json
│   │   ├── chapter-02.json
│   │   └── chapter-03.json
│   ├── voices.json         # danh sách voice đã duyệt kèm license/attribution
│   └── audio-manifest.json # danh mục sinh audio chi tiết
│
├── content-md/
│   ├── CHAPTER_01_CONTENT.md
│   ├── CHAPTER_02_CONTENT.md
│   └── CHAPTER_03_CONTENT.md
│
├── audio/                  # MP3 phát hành, được commit
│   ├── chapter-01/
│   ├── chapter-02/
│   └── chapter-03/
│
├── images/
│   └── chapter-02/         # 18 ảnh SVG minh họa cho Part 1
│
├── scripts/
│   ├── generate_audio.py   # script sinh audio CBR mono và bù offset
│   ├── voice_audition.py   # kiểm tra audition voice và in rõ license/credit
│   ├── check_content.py    # validator kiểm tra toàn diện dữ liệu và liên kết
│   └── requirements.txt
│
└── tests/
    └── progress-test.html  # trang tự động chạy kiểm thử nghiệm thu lưu trữ
```

**Quy tắc đường dẫn:** Mọi URL trong HTML, CSS, JS, JSON đều là đường dẫn tương đối (ví dụ `data/...`, `audio/...`, `css/...`), tuyệt đối không bắt đầu bằng `/`. Tên file và thư mục luôn viết thường không dấu cách.

---

## 4. Chạy và triển khai

### 4.1. Chạy local khi phát triển
```bash
python -m http.server 8000
```
Mở trình duyệt truy cập `http://localhost:8000`.

### 4.2. Triển khai GitHub Pages
1. Đẩy mã nguồn lên branch `main` của repo public `https://github.com/hp0705/Toeic_Listen.git`.
2. Truy cập Settings → Pages → chọn Deploy from a branch: `main` / `(root)`.
3. Trang web hoạt động tại `https://hp0705.github.io/Toeic_Listen/`.

---

## 5. Thiết kế giao diện và trải nghiệm học (Mobile-First)

Ứng dụng được tối ưu hóa cho màn hình cảm ứng di động và máy tính:
- Nút bấm lớn (tối thiểu 48px), khoảng cách an toàn, dễ chạm ngón tay.
- Giao diện gồm 5 màn hình chính:
  1. **Dashboard:** Tổng quan mục tiêu 300, tiến độ các chương, nút "Tiếp tục học", thẻ nhắc sao lưu nếu cần.
  2. **Learning Path:** Bản đồ toàn khóa, trạng thái từng bài (Đã học / Đang học / Chưa mở), điều kiện qua bài.
  3. **Lesson View:** Trình bày giáo trình tiếng Việt, ví dụ audio, bảng từ vựng, nút vào làm bài luyện hoặc bài kiểm tra.
  4. **Quiz / Practice View:**
     - Player âm thanh trung tâm với thanh điều khiển tốc độ (1.0x và 0.85x trong Learn Mode).
     - Với Part 1 & Part 2: Chỉ hiển thị các nút lựa chọn A, B, C (hoặc D) không có chữ (`optionsVisibleBeforeAnswer: false`). Sau khi người học chọn, văn bản lựa chọn và giải thích mới hiện ra.
     - Với Foundation (CH01-L01..L03) và Part 3: Hiển thị câu hỏi tiếng Việt/tiếng Anh và các phương án trên màn hình để người học đọc trước (`optionsVisibleBeforeAnswer: true`).
     - Với Part 3: Hiển thị trọn vẹn cụm 3 câu hỏi thuộc cùng một đoạn hội thoại (`groupId`).
     - Xáo trộn thứ tự phương án mỗi lần làm nhưng giữ ổn định khi tải lại trang qua `optionOrder`.
     - Phân tích đáp án đúng và lý do sai của từng distractor ngay sau khi nộp câu trả lời (Learn Mode) hoặc sau khi nộp bài test (Test Mode).
     - Cho phép người học tự đánh dấu lý do sai vào Sổ lỗi.
  5. **Mistake Book (Sổ lỗi):**
     - Liệt kê các câu hỏi sai cần ôn tập.
     - Lọc theo `skillGroup` và trạng thái (Cần ôn / Đang luyện / Đã khắc phục).
     - Cung cấp nút "Luyện câu mới cùng nhóm kỹ năng" để người học giải quyết lỗi dứt điểm.
  6. **Lịch sử & Sao lưu (History & Backup):**
     - Dòng thời gian chi tiết các lượt học.
     - Nút Xuất file JSON, Nhập Gộp (Merge), Nhập Thay thế (Replace) kèm nút Hoàn tác (Undo).

---

## 6. Phân biệt phiên bản: `specVersion` và `contentVersion`

Để tránh nhầm lẫn giữa cấu trúc kỹ thuật và nội dung bài học:
- **`specVersion` (Phiên bản đặc tả kỹ thuật):** Đại diện cho quy chuẩn kiến trúc phần mềm, schema JSON và hành vi của web app. Hiện tại là `"2.3"`.
- **`contentVersion` (Phiên bản nội dung):** Đại diện cho bộ câu hỏi, giáo trình và audio bài học. Hiện tại là `"1.0.0"`.

---

## 7. Schema dữ liệu JSON

### 7.1. `data/course.json`
```json
{
  "courseId": "toeic-listening-300",
  "title": "TOEIC Listening 300",
  "targetScore": 300,
  "scoreScale": 495,
  "specVersion": "2.3",
  "contentVersion": "1.0.0",
  "chapters": [
    {
      "id": "CH01",
      "file": "chapters/chapter-01.json",
      "title": "Nền tảng nghe",
      "description": "Bắt từ khóa, âm cuối, số giờ và ý câu hỏi",
      "unlock": "default"
    },
    {
      "id": "CH02",
      "file": "chapters/chapter-02.json",
      "title": "Part 1 & Part 2 mở rộng",
      "description": "Mô tả tranh, câu hỏi gián tiếp và phản hồi tự nhiên",
      "unlock": "CH01_PASS"
    },
    {
      "id": "CH03",
      "file": "chapters/chapter-03.json",
      "title": "Part 3 cơ bản: hội thoại hai người",
      "description": "Mục đích, địa điểm, chi tiết, vấn đề và hành động tiếp theo",
      "unlock": "CH02_PASS"
    }
  ]
}
```

### 7.2. Quy tắc `passRule` tường minh cho từng Lesson
Trong `data/chapters/*.json`, mỗi lesson khai báo trường `passRule` rõ ràng để loại bỏ mâu thuẫn tỷ lệ 80%:

```json
"passRule": {
  "minCorrect": 3,
  "total": 4,
  "percentage": 75
}
```

Bảng cấu hình `passRule` chuẩn:
- Bài 4 câu (CH01-L01, CH01-L02, CH02-L01, CH02-L02, CH02-L03): `{"minCorrect": 3, "total": 4, "percentage": 75}`
- Bài 5 câu (CH01-L03, CH01-L04): `{"minCorrect": 4, "total": 5, "percentage": 80}`
- Bài 6 câu (CH02-L04, CH03-L01 đến CH03-L05): `{"minCorrect": 5, "total": 6, "percentage": 83.3}`
- Bài 8 câu (CH02-L05): `{"minCorrect": 6, "total": 8, "percentage": 75}`
- Bài 12 câu (CH01-L05): `{"minCorrect": 10, "total": 12, "percentage": 83.3}`
- Bài Final Test 15 câu (CH01-FINAL, CH02-FINAL): `{"minCorrect": 12, "total": 15, "percentage": 80}`
- Bài Final Test 12 câu (CH03-FINAL): `{"minCorrect": 10, "total": 12, "percentage": 83.3}`

### 7.3. Schema Question chuẩn (Hỗ trợ Foundation, Part 1, Part 2)
```json
{
  "id": "CH01-L01-Q01",
  "chapterId": "CH01",
  "lessonId": "CH01-L01",
  "part": 0,
  "taskType": "foundation_listening",
  "prompt": "Khi nào người quản lý gửi báo cáo?",
  "optionsVisibleBeforeAnswer": true,
  "image": null,
  "audioSegments": [
    {
      "text": "The manager will send the report tomorrow.",
      "voice": "us-female-01",
      "file": "audio/chapter-01/ch01-l01-q01.mp3",
      "pauseAfterMs": 0
    }
  ],
  "options": {
    "A": "This afternoon",
    "B": "Tomorrow",
    "C": "Next week"
  },
  "correctAnswer": "B",
  "transcript": "The manager will send the report tomorrow.",
  "translation": "Người quản lý sẽ gửi báo cáo vào ngày mai.",
  "explanation": "tomorrow là mốc thời gian được nói trực tiếp trong audio.",
  "wrongReasons": {
    "A": "This afternoon (chiều nay) không xuất hiện trong câu.",
    "C": "Next week (tuần sau) không được nhắc đến."
  },
  "skillTags": ["time_expression", "keyword_listening"],
  "skillGroup": "time_and_numbers",
  "difficulty": 1,
  "revision": 1
}
```

Với Part 1 & Part 2, trường `optionsVisibleBeforeAnswer` được đặt là `false`:
```json
{
  "id": "CH02-L01-Q01",
  "chapterId": "CH02",
  "lessonId": "CH02-L01",
  "part": 1,
  "taskType": "photograph_description",
  "prompt": "Nghe 4 câu mô tả và chọn câu đúng nhất cho bức tranh.",
  "optionsVisibleBeforeAnswer": false,
  "image": "images/chapter-02/ch02-l01-q01.svg",
  "audioSegments": [
    {"text": "A man is typing on a computer.", "choiceId": "A", "file": "audio/chapter-02/ch02-l01-q01-01.mp3", "pauseAfterMs": 500},
    {"text": "A man is drinking from a cup.", "choiceId": "B", "file": "audio/chapter-02/ch02-l01-q01-02.mp3", "pauseAfterMs": 500},
    {"text": "A man is walking to the door.", "choiceId": "C", "file": "audio/chapter-02/ch02-l01-q01-03.mp3", "pauseAfterMs": 500},
    {"text": "A man is writing in a notebook.", "choiceId": "D", "file": "audio/chapter-02/ch02-l01-q01-04.mp3", "pauseAfterMs": 0}
  ],
  "options": {
    "A": "A man is typing on a computer.",
    "B": "A man is drinking from a cup.",
    "C": "A man is walking to the door.",
    "D": "A man is writing in a notebook."
  },
  "correctAnswer": "A",
  "transcript": "(A) A man is typing on a computer. (B) A man is drinking from a cup. (C) A man is walking to the door. (D) A man is writing in a notebook.",
  "translation": "(A) Người đàn ông đang gõ máy tính. (B) Đang uống nước. (C) Đang đi ra cửa. (D) Đang viết sổ.",
  "explanation": "Tranh mô tả người đàn ông đang ngồi gõ bàn phím máy tính.",
  "wrongReasons": {
    "B": "Không có cốc nước nào trong tay.",
    "C": "Người đàn ông đang ngồi, không hề đi lại.",
    "D": "Tay đặt trên bàn phím máy tính, không cầm bút viết sổ."
  },
  "skillTags": ["part1_action_verbs", "present_continuous"],
  "skillGroup": "part1_photographs",
  "difficulty": 1,
  "revision": 1
}
```

### 7.4. Schema Nhóm Part 3 (`groups[]`) và Question liên kết
Định dạng ID nhóm được chuẩn hóa thống nhất là `CH03-Lxx-Gyy`:

```json
{
  "id": "CH03-L01-G01",
  "chapterId": "CH03",
  "lessonId": "CH03-L01",
  "part": 3,
  "groupType": "conversation",
  "context": "Một khách hàng gọi cho nhân viên cửa hàng in ấn",
  "speakers": [
    {"speakerId": "W1", "label": "Woman", "gender": "female"},
    {"speakerId": "M1", "label": "Man", "gender": "male"}
  ],
  "voiceAssignment": {"W1": "us-female-01", "M1": "us-male-01"},
  "turns": [
    {"turn": 1, "speakerId": "W1", "text": "Hello, this is Carla Mendes from Brightwell Dental.", "pauseAfterMs": 450, "startMs": 0, "endMs": 2800},
    {"turn": 2, "speakerId": "M1", "text": "Hello, Ms. Mendes. How can I help you today?", "pauseAfterMs": 450, "startMs": 3250, "endMs": 5900}
  ],
  "audioFile": "audio/chapter-03/ch03-l01-g01.mp3",
  "transcript": "W1: Hello, this is Carla Mendes from Brightwell Dental. / M1: Hello, Ms. Mendes. How can I help you today?",
  "translation": "W1: Xin chào, tôi là Carla Mendes từ Brightwell Dental. / M1: Chào cô Mendes. Tôi có thể giúp gì cho cô hôm nay?",
  "questionIds": ["CH03-L01-Q01", "CH03-L01-Q02", "CH03-L01-Q03"],
  "revision": 1
}
```

Câu hỏi liên kết với group Part 3:
```json
{
  "id": "CH03-L01-Q01",
  "groupId": "CH03-L01-G01",
  "chapterId": "CH03",
  "lessonId": "CH03-L01",
  "part": 3,
  "taskType": "conversation_question",
  "prompt": "Why is the woman calling?",
  "optionsVisibleBeforeAnswer": true,
  "options": {
    "A": "To cancel an order",
    "B": "To change a delivery address",
    "C": "To check the status of an order",
    "D": "To complain about a price"
  },
  "correctAnswer": "C",
  "explanation": "Người phụ nữ nói 'I'm calling to see if our brochure order is ready', tức kiểm tra đơn hàng.",
  "wrongReasons": {
    "A": "Cô ấy không yêu cầu hủy đơn hàng.",
    "B": "Địa chỉ giao hàng không được đề cập.",
    "D": "Không có lời phàn nàn nào về giá cả."
  },
  "skillTags": ["part3_purpose", "part3_paraphrase"],
  "skillGroup": "part3_conversations",
  "difficulty": 1,
  "revision": 1
}
```

---

## 8. Tiêu chuẩn âm thanh và bản quyền giọng đọc

### 8.1. Mã hóa MP3 CBR và bù sai lệch thời gian (Offset Compensation)
- **Bắt buộc mã hóa CBR (Constant Bitrate)**: Mã hóa MP3 với bitrate cố định (ví dụ 64 kbps hoặc 128 kbps CBR mono, sample rate 24kHz hoặc 44.1kHz). Tuyệt đối **không dùng VBR (Variable Bitrate)** vì VBR khiến trình duyệt ước lượng sai `currentTime` khi tìm kiếm vị trí (seek).
- **Bù sai lệch encoder delay**: Khi chuyển đổi âm thanh sang MP3, các bộ mã hóa (như LAME) thường thêm một đoạn trễ nhỏ (encoder delay / padding khoảng vài chục ms). Script tạo audio phải tính toán bù trừ độ trễ này để `startMs` và `endMs` trong JSON khớp chuẩn xác với điểm phát thực tế của từng lượt thoại trong phạm vi sai số dưới 150 ms.

### 8.2. Quy định nghiêm ngặt về bản quyền giọng đọc (Voice Licensing)
- Vì ứng dụng được đưa lên kho mã nguồn công khai (Public GitHub Repository), **chỉ chấp nhận các mô hình giọng đọc có giấy phép (license) cho phép phát hành lại âm thanh đã tổng hợp một cách công khai** (ví dụ MIT, Apache 2.0, Open Data Commons, hoặc giấy phép tương đương cho phép public redistribution).
- Script `scripts/voice_audition.py` bắt buộc phải trích xuất và hiển thị rõ ràng: ID giọng, Giới tính, Tên tác giả, Giấy phép bản quyền (License) và Điều khoản ghi nhận công lao (Attribution requirements).
- `data/voices.json` lưu trữ chi tiết trường `license` và `credit`. Nếu voice yêu cầu ghi nhận quyền tác giả, thông tin này phải được tự động hiển thị trong trang Thông tin & Bản quyền của ứng dụng.

---

## 9. Hướng dẫn xác thực và nghiệm thu

File `scripts/check_content.py` và trang kiểm tra `tests/progress-test.html` là bộ kiểm thử nghiệm thu chính:
- Kiểm tra toàn bộ tính toàn vẹn của JSON: Không trùng lặp ID, mọi câu hỏi đều có giải thích đúng và giải thích các distractor, tất cả đường dẫn audio và hình ảnh tham chiếu đều có thật.
- Kiểm tra `passRule` của mọi bài học được định nghĩa tường minh và chính xác.
- Kiểm tra `skillGroup` tồn tại trên tất cả câu hỏi và hỗ trợ cơ chế khắc phục lỗi.
- Đảm bảo app chạy mượt mà trên cả trình duyệt máy tính và di động, tuân thủ 100% tiêu chí bảo vệ quyền riêng tư và hoạt động độc lập không phụ thuộc mạng ngoài.
