# SPEC UPDATE NOTES — v2.2

Cơ sở cập nhật: `SPEC_WEB_APP(1).md` (v2.1) và nội dung patch do người học gửi.

## Đã đưa vào spec

- `groups[]` cho Part 3/4; mỗi hội thoại/bài nói liên kết với ba câu hỏi.
- Part 3 MVP có một speaker nữ và một speaker nam; voice gán theo speaker, không đổi trong cùng hội thoại.
- `data/voices.json` lưu voice ID thực, giới tính, accent, license/credit và trạng thái duyệt.
- Script audition nghe thử voice trước; chỉ dùng voice đã duyệt.
- Sinh từng lượt thoại riêng, ghép thành một MP3/group, lưu timestamp để replay từng lượt trong Learn Mode.
- Không pitch shift, không TTS cloud, không API key, không gửi text ra ngoài.
- Ghi `groupId` vào attempts và `optionOrder` để xem lại lựa chọn đã xáo.
- Bắt buộc xáo đáp án vì answer key CH01/CH02 hiện lệch A nghiêm trọng.

## Đã đơn giản hóa so với patch đề xuất

- MVP chỉ tải một voice nữ + một voice nam; patch gợi ý hai voice mỗi giới. Có thể bổ sung voice phụ sau để giảm tải model và dung lượng ban đầu.
- Không đưa Gemini TTS làm fallback vì yêu cầu hiện tại là hoàn toàn miễn phí và offline.
- Không đánh dấu CH03 đã có nội dung: file `CHAPTER_03_CONTENT.md` không nằm trong các tệp được gửi ở lượt này.
- Sửa ý tưởng chèn nội dung Part 3/4 thành các bullet độc lập; không dùng cách chèn dòng có nguy cơ làm vỡ bullet Part 2.

## Nguồn kiểm tra API

Tài liệu chính thức `loudness-tts` hiện nêu API liệt kê voice theo `language` và `sex`, API tổng hợp chỉ định `voice` và `speed`, voice metadata có license/credit. Gemini phải kiểm tra API thực tế của phiên bản đã cài và không tự đoán field/tên hàm.
