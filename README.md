# TOEIC Listening 300 — Spec Pack (v2.3)

Bộ tài liệu để xây một web app luyện TOEIC Listening **miễn phí**, dùng được trên điện thoại và máy tính qua trình duyệt, host bằng **GitHub Pages**.

- Repo: https://github.com/hp0705/Toeic_Listen.git
- Website (sau khi bật Pages): https://hp0705.github.io/Toeic_Listen/

## Đọc theo thứ tự

1. `SPEC_WEB_APP.md` — công nghệ, cấu trúc source, giao diện, JSON, audio MP3 CBR, xáo đáp án, optionsVisibleBeforeAnswer, triển khai GitHub Pages, nghiệm thu.
2. `PROGRESS_STORAGE_SPEC.md` — **cách lưu lịch sử học**, sao lưu, nhập/gộp tiến độ, cơ chế khắc phục lỗi theo `skillGroup`, kiểm thử. Nguồn chuẩn cho mọi thứ liên quan tiến độ.
3. `CHAPTER_01_CONTENT.md` — giáo trình Chương 1 (Nền tảng nghe, 45 câu).
4. `CHAPTER_02_CONTENT.md` — giáo trình Chương 2 (Part 1 & 2 mở rộng, 41 câu, 18 ảnh SVG).
5. `CHAPTER_03_CONTENT.md` — giáo trình Chương 3 (Part 3 cơ bản: hội thoại 2 người, 14 hội thoại, 42 câu).
6. `CONTENT_REGISTRY.md` — quản lý nội dung đã tạo, trạng thái audio và quy trình cập nhật.

## Phiên bản hệ thống

- **Phiên bản Spec (`specVersion`):** 2.3
- **Phiên bản Nội dung (`contentVersion`):** 1.0.0 (bao gồm CH01, CH02, CH03 đầy đủ)

## Quan trọng

Bundle này hiện đã có đủ Markdown spec và giáo trình CH01, CH02, CH03. Source web app được xây dựng theo chuẩn static web (HTML5/CSS3/Vanilla JS ES6+), không cần build step, tương thích hoàn hảo GitHub Pages và chạy mượt mà trên trình duyệt di động lẫn máy tính.

## Điểm cần nhớ

- Lịch sử học lưu **trong trình duyệt của từng thiết bị** (LocalStorage), không lưu trên GitHub. Hãy **xuất sao lưu định kỳ**; dùng nhiều thiết bị thì nhập bằng chế độ **Gộp**.
- Repo public: không commit file tiến độ (`.gitignore` đã chặn), không đưa API key vào source.
- Audio phát hành bằng MP3 CBR (chuẩn hóa sample rate, bù encoder delay).
- Mọi đường dẫn tương đối; tên file viết thường.

## Phát triển local

```bash
python -m http.server 8000
```

Mở `http://localhost:8000`.

## Triển khai

1. Push toàn bộ source lên branch `main`.
2. GitHub → Settings → Pages → Deploy from a branch → `main` / `(root)`.
3. Mở link Pages trên điện thoại thật và máy tính, chạy checklist nghiệm thu trong `SPEC_WEB_APP.md`.
