@echo off
echo Building yt-downloader...
pyinstaller --name "yt-downloader-gui" ^
  --windowed ^
  --icon=favicon.ico ^
  main.py
pause
