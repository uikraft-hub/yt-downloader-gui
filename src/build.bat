@echo off
echo Building yt-downloader...
pyinstaller --name "yt-downloader-gui" ^
  --windowed ^
  --icon=favicon.ico ^
  yt-downloader-gui.py
pause
