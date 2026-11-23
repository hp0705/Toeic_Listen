# SPEC UPDATE NOTES — v2.3

Cơ sở cập nhật: Hoàn thiện tích hợp Chương 3 (CH03) và giải quyết triệt để 12 điểm phản hồi từ người học trước khi lập trình.

## Các nội dung đã hoàn thiện và cập nhật trong v2.3:

1. **Cập nhật đồng bộ sau khi có CH03:**
   - Đưa `CHAPTER_03_CONTENT.md` vào toàn bộ danh mục tài liệu (`README.md`, `CONTENT_REGISTRY.md`, `SPEC_WEB_APP.md`).
   - Cập nhật `CONTENT_REGISTRY.md` phản ánh đúng trạng thái đã có đầy đủ 14 hội thoại và 42 câu hỏi của CH03.

2. **Tách biệt rõ ràng phiên bản đặc tả kỹ thuật và phiên bản nội dung:**
   - `specVersion`: "2.3" (quy chuẩn kiến trúc app, schema JSON, logic lưu trữ).
   - `contentVersion`: "1.0.0" (bộ dữ liệu giáo trình CH01, CH02, CH03).

3. **Giải quyết triệt để mâu thuẫn ngưỡng đạt 80% (`passRule` tường minh):**
   - Bổ sung cấu trúc `passRule: { minCorrect, total, percentage }` vào từng lesson trong file chapter JSON.
   - Các bài 4 câu: yêu cầu 3/4 (75%).
   - Các bài 8 câu (CH02-L05): yêu cầu 6/8 (75%).
   - Các bài 5 câu: 4/5 (80%); bài 6 câu: 5/6 (83.3%); bài 12 câu: 10/12 (83.3%); Final test 15 câu: 12/15 (80%); Final test 12 câu: 10/12 (83.3%).

4. **Cơ chế khắc phục lỗi dứt điểm với `skillGroup`:**
   - Bổ sung trường `skillGroup` cho mọi câu hỏi.
   - Một lỗi được coi là đã khắc phục khi người học làm đúng một câu hỏi mới (ở 1.0x, không xem transcript trước) có cùng `skillTag` HOẶC cùng `skillGroup` (với Part 3 phải khác `groupId`). Giải quyết triệt để vấn đề các tag chỉ xuất hiện một lần.

5. **Hoàn thiện schema câu hỏi CH01 và ẩn lựa chọn trước khi trả lời (`optionsVisibleBeforeAnswer`):**
   - Bổ sung schema câu hỏi Foundation cho CH01-L01..L03 với `taskType: "foundation_listening"` và `prompt` tiếng Việt.
   - Thêm trường `optionsVisibleBeforeAnswer`: Đặt là `false` cho Part 1 & Part 2 để người học buộc phải nghe audio thay vì đọc chữ trên màn hình; đặt là `true` cho Foundation và Part 3/4.

6. **Chuẩn hóa đồng nhất Group ID Part 3:**
   - Chuẩn hóa toàn bộ mã nhóm sang định dạng `CH03-Lxx-Gyy` (thay thế triệt để các mã cũ `-C01`, `-C02`).

7. **Chuẩn hóa mã hóa MP3 CBR và bù sai lệch thời gian (Offset Compensation):**
   - Bắt buộc mã hóa MP3 CBR (Constant Bitrate) mono, loại trừ hoàn toàn sai lệch thời gian của VBR.
   - Bù trừ độ trễ encoder delay đảm bảo độ chính xác của timestamp dưới 150 ms.

8. **Quy định nghiêm ngặt về giấy phép bản quyền giọng đọc (Voice Licensing):**
   - Chỉ duyệt các voice có license cho phép phát hành công khai audio tổng hợp lên public repository.
   - `scripts/voice_audition.py` in rõ ràng thông tin license, tác giả và điều khoản attribution.
