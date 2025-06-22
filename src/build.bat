@echo off
echo Building Youtube Media Downloader...
pyinstaller --name "YMD" ^
  --windowed ^
  --icon=favicon.ico ^
  main.py
pause
