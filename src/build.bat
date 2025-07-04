@echo off
echo Building yt-downloader...
pyinstaller --name "yt-downloader" ^
  --windowed ^
  --icon=favicon.ico ^
  yt-downloader.py
pause
