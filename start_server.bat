@echo off
chcp 65001 > nul
title TOEIC Listening 300 - Local Server
echo ======================================================================
echo   TOEIC Listening 300 - Máy chủ Web cục bộ (Local Server)
echo ======================================================================
echo.
echo Đang khởi động máy chủ tại: http://localhost:8000
echo.
echo [MẸO]: Nếu trình duyệt từng lưu cache của dự án khác, hãy nhấn Ctrl + Shift + R
echo để tải mới hoàn toàn.
echo.
echo Nhấn Ctrl + C để dừng máy chủ bất kỳ lúc nào.
echo ======================================================================
start http://localhost:8000
python -m http.server 8000
pause
