# PROGRESS STORAGE SPEC — TOEIC LISTENING 300

**Phiên bản Spec (`specVersion`):** 2.3 (đi cùng `SPEC_WEB_APP.md` v2.3)  
**Phiên bản Schema (`schemaVersion`):** 2  
**Phiên bản Nội dung mặc định (`contentVersion`):** 1.0.0  
**Mục tiêu:** lưu tiến độ cục bộ, không tài khoản, không cloud, có sao lưu/khôi phục và gộp giữa thiết bị.

---

## 1. Nguyên tắc

- Dùng `localStorage`; không cần database hoặc backend.
- Không đưa dữ liệu học cá nhân vào GitHub (repo public).
- Lưu lịch sử lượt làm bài (`runs`) và lượt trả lời (`attempts`) dưới dạng bản ghi bất biến có ID duy nhất; dữ liệu tổng hợp (tiến độ bài, mở khóa, sổ lỗi) được tính lại từ lịch sử (`rebuildDerived`).
- Không gọi `localStorage.clear()` vì GitHub Pages có thể cùng origin với các ứng dụng khác của cùng tài khoản người dùng.
- Mọi key phải có tiền tố `toeic_listening_300`.

---

## 2. Key và schema

Key chính trong LocalStorage: `toeic_listening_300_v2`.  
Dữ liệu lưu trữ:

```json
{
  "schemaVersion": 2,
  "specVersion": "2.3",
  "courseId": "toeic-listening-300",
  "contentVersion": "1.0.0",
  "updatedAt": "2026-11-23T00:00:00.000Z",
  "runs": [],
  "attempts": [],
  "settings": {
    "lastBackupAt": null,
    "remindBackup": true
  }
}
```

Key lưu snapshot dự phòng tức thời trước khi ghi: `toeic_listening_300_backup_last`.

---

## 3. Run record

Một `run` là một phiên người học thực hiện một bài học (`lesson`) hoặc bài kiểm tra (`finalTest`). Bắt buộc có:

- `id`: ID duy nhất dạng UUID v4 hoặc `run-{timestamp}-{random}`.
- `chapterId`: ví dụ `"CH01"`, `"CH02"`, `"CH03"`.
- `lessonId`: ví dụ `"CH01-L01"`, `"CH01-FINAL"`.
- `mode`: `"learn"` hoặc `"test"`.
- `startedAt`: chuỗi ISO 8601.
- `finishedAt`: chuỗi ISO 8601 hoặc `null` nếu đang làm.
- `status`: `"in_progress"`, `"submitted"`, `"abandoned"`.
- `optionOrders`: map ánh xạ từ `questionId` sang mảng các ID đáp án gốc theo thứ tự hiển thị ngẫu nhiên trên màn hình (ví dụ `{"CH01-L01-Q01": ["B", "A", "C"]}`). Tạo và lưu ngay khi khởi tạo run để việc refresh trang không làm thay đổi vị trí lựa chọn.

---

## 4. Attempt record

Mỗi câu trả lời tạo một `attempt` riêng biệt và bất biến:

```json
{
  "id": "attempt-unique-id",
  "runId": "run-unique-id",
  "questionId": "CH03-L01-Q01",
  "groupId": "CH03-L01-G01",
  "chapterId": "CH03",
  "lessonId": "CH03-L01",
  "part": 3,
  "mode": "learn",
  "selected": "C",
  "optionOrder": ["B", "A", "C", "D"],
  "isCorrect": true,
  "questionRevision": 1,
  "answeredAt": "2026-11-23T00:00:00.000Z",
  "transcriptViewedBeforeAnswer": false,
  "playbackRate": 1.0,
  "mistakeGroup": null
}
```

Quy tắc:

- `selected`: Luôn lưu ID đáp án gốc trong JSON (ví dụ `"A"`, `"B"`, `"C"` gốc), không phải chữ cái hiển thị tạm thời trên giao diện.
- `optionOrder`: Lưu thứ tự các ID gốc tương ứng với nhãn A/B/C/D đang hiển thị trên nút bấm của người học.
- `isCorrect`: Được tính bằng cách lấy ID gốc của phương án người học vừa bấm thông qua `optionOrder`, so sánh với `correctAnswer` gốc.
- `groupId`: ID group Part 3/4 (chuẩn hóa dạng `CH03-Lxx-Gxx`); đối với câu hỏi đơn lẻ Part 1/2 hoặc Foundation thì `groupId: null`.
- `mistakeGroup`: Nhóm khó khăn người học tự chọn nếu trả lời sai (ví dụ `"missed_sound"`, `"vocabulary"`, `"distractor"`...).
- Attempt không bị sửa đè; làm lại sẽ tạo attempt mới.

---

## 5. Dữ liệu dẫn xuất (`rebuildDerived`)

Không lưu cờ hoàn thành/mở khóa như nguồn chân lý duy nhất. Hàm `rebuildDerived(state, courseData)` dựng lại toàn bộ trạng thái học tập từ danh sách `runs` và `attempts`:

1. **Lesson Progress & Pass Status:**
   - Mỗi bài học (`lesson`) được đánh dấu hoàn thành (`passed: true`) khi có ít nhất một run hoàn thành (`submitted`) đạt ngưỡng quy định bởi `passRule` của bài đó (được định nghĩa tường minh trong `chapter-*.json`).
   - Nếu `passRule` quy định `minCorrect: 3, totalQuestions: 4` (75%), bài sẽ đạt ngay khi đúng từ 3 câu trở lên.
2. **Chapter Unlock Status:**
   - CH01: Mở mặc định (`unlock: "default"`).
   - CH02: Mở khi hoàn thành bài `CH01-FINAL` đạt từ 80% trở lên (12/15 câu).
   - CH03: Mở khi hoàn thành bài `CH02-FINAL` đạt từ 80% trở lên (12/15 câu).
3. **Thống kê kỹ năng & Sổ lỗi (Mistake Book):**
   - Tập hợp các câu hỏi từng làm sai lần gần nhất.
   - Thống kê tỷ lệ chính xác tổng thể và theo từng `skillTag` cũng như `skillGroup`.

---

## 6. Sổ lỗi và cơ chế khắc phục lỗi (`skillGroup`)

### Vấn đề thực tế
Nhiều tag kỹ năng chuyên biệt chỉ xuất hiện một lần trong suốt giáo trình (ví dụ: `contraction_weve`, `quarter_to`, `final_sound_s`, `ed_ending`). Nếu bắt buộc phải có câu mới có *cùng đúng `skillTag` đó* thì người học sẽ **vĩnh viễn không bao giờ khắc phục được lỗi**.

### Giải pháp đa tầng với `skillGroup`
Mỗi câu hỏi trong JSON được gắn cả `skillTags[]` và một `skillGroup` bao quát.
Ví dụ:
- Câu có tag `contraction_weve` thuộc nhóm `skillGroup: "contractions"`.
- Câu có tag `quarter_to` thuộc nhóm `skillGroup: "numbers_and_time"`.
- Câu có tag `final_sound_s`, `ed_ending` thuộc nhóm `skillGroup: "word_endings"`.

### Điều kiện để một câu sai chuyển sang trạng thái "Đã khắc phục" (`resolved`):
1. Người học thực hiện một câu hỏi mới **khác với câu đã làm sai**.
2. Câu mới này có **cùng `skillTag` HOẶC cùng `skillGroup`** với câu sai.
3. Đối với Part 3/4, câu mới phải thuộc **`groupId` khác** (không được dùng câu hỏi trong cùng một đoạn hội thoại để xóa lỗi).
4. Người học trả lời **đúng** ở tốc độ chuẩn **1.0x**.
5. Người học **không bấm xem transcript** trước khi gửi câu trả lời.

Nếu người học sau đó làm lại chính câu đó mà lại chọn sai, trạng thái câu hỏi sẽ quay về `"needs_review"`.

---

## 7. Lưu an toàn

- Ghi state vào LocalStorage ngay sau mỗi attempt và khi run chuyển trạng thái (`started`, `submitted`).
- Trước khi ghi đè, sao lưu dữ liệu hiện tại vào key `toeic_listening_300_backup_last`.
- Xử lý ngoại lệ `QuotaExceededError`: hiển thị thông báo khuyên người học xuất file sao lưu, tuyệt đối không âm thầm xóa lịch sử.
- Đa tab: kiểm tra `updatedAt` trước khi ghi; nếu phát hiện dữ liệu LocalStorage mới hơn state trong bộ nhớ thì hòa trộn (merge) thay vì ghi đè mất mát.

---

## 8. Sao lưu và khôi phục

### Nhắc nhở định kỳ
Hiển thị banner nhắc người học xuất bản sao lưu khi:
- Chưa từng sao lưu lần nào và đã thực hiện trên 20 attempts.
- Hoặc đã quá 7 ngày kể từ lần sao lưu gần nhất.

### Cấu trúc file xuất JSON
```json
{
  "schemaVersion": 2,
  "specVersion": "2.3",
  "contentVersion": "1.0.0",
  "courseId": "toeic-listening-300",
  "exportedAt": "2026-11-23T09:30:00.000Z",
  "runs": [...],
  "attempts": [...],
  "settings": {...},
  "coachSummary": {
    "totalAttempts": 120,
    "accuracy": 0.82,
    "chaptersCompleted": ["CH01", "CH02"],
    "currentUnlockedChapter": "CH03",
    "openMistakesCount": 4,
    "weakSkillGroups": ["contractions", "indirect_response"],
    "strongSkillGroups": ["time_expression", "who_questions"]
  }
}
```

### Chế độ nhập (Import):
1. **Gộp (Merge - Mặc định):**
   - Kết hợp các `runs` và `attempts` từ file vào LocalStorage theo `id`. Bản ghi nào đã có thì giữ nguyên, bản ghi mới thì thêm vào.
   - Không làm mất bất kỳ dữ liệu học tập nào hiện có trên máy.
2. **Thay thế (Replace):**
   - Ghi đè toàn bộ dữ liệu hiện tại bằng dữ liệu trong file.
   - Tự động lưu bản sao lưu khôi phục vào `toeic_listening_300_backup_last` để có thể bấm "Hoàn tác" ngay lập tức nếu nhầm lẫn.

---

## 9. Danh mục kiểm thử nghiệm thu lưu trữ

Trang kiểm thử `tests/progress-test.html` phải tự động chạy và vượt qua toàn bộ các ca kiểm thử sau:
- [ ] Khởi tạo state mặc định khi chưa có dữ liệu.
- [ ] Ghi nhận run và attempt, refresh trang dữ liệu vẫn nguyên vẹn.
- [ ] Ánh xạ `optionOrder` sau xáo đáp án vẫn chấm chính xác theo ID đáp án gốc.
- [ ] Attempt Part 3 lưu đúng `groupId` dạng `CH03-Lxx-Gxx`.
- [ ] Ba câu trong cùng một group Part 3 sinh ra ba attempt độc lập cùng chung `groupId`.
- [ ] `rebuildDerived` tính đúng trạng thái pass cho bài 4 câu (đạt 3/4 = 75%) và bài 8 câu (đạt 6/8 = 75%).
- [ ] Mở khóa CH02 khi CH01 đạt Final Test >= 80%, mở khóa CH03 khi CH02 đạt Final Test >= 80%.
- [ ] Cơ chế khắc phục lỗi nhận diện thành công câu đúng cùng `skillGroup` (thay vì chỉ cùng `skillTag`).
- [ ] Câu hỏi trong cùng `groupId` Part 3 không được công nhận là câu khắc phục lỗi cho nhau.
- [ ] Nhập file chế độ Gộp (Merge) không tạo bản ghi trùng lặp và giữ nguyên các lần làm bài hiện có.
- [ ] Nhập file chế độ Thay thế (Replace) cho phép Hoàn tác khôi phục trạng thái trước đó.
- [ ] Không có bất kỳ dòng code nào gọi `localStorage.clear()`.
