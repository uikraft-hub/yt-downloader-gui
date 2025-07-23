# yt-downloader-gui v2.4.0

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE) [![Language: Python](https://img.shields.io/badge/Language-Python-blue.svg)](#) [![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen.svg)](#)

<p align="center">
  <img src="src/favicon.ico" alt="App Icon" width="64" height="64" />
</p>

**yt-downloader-gui** is a powerful, open‑source desktop application built with PyQt6 and yt-dlp that lets you download single videos, playlists, channels (videos & shorts), or just MP3 audio—seamlessly and reliably.

---

## 🆕 What’s New in v2.4.0

- **Professional UI Redesign**
  - Complete visual overhaul with a new professional dark theme.
  - Consistent styling across all widgets using a dedicated QSS stylesheet.
  - Improved layout with a larger default window size for a better user experience.
- **Enhanced Download Progress**
  - Added a visual progress bar to the "Activity" page for real-time download feedback.
  - The progress bar is updated dynamically by parsing `yt-dlp`'s output.
- **Code Refinements**
  - Removed all inline styling in favor of the new stylesheet.
  - Added object names to widgets for more specific styling.
  - Updated version number to 2.4.0 in the "About" dialog.

---

## ⭐ Features

- **Automatic yt‑dlp Updater**  
  Checks GitHub for new yt-dlp releases and replaces your local binary automatically.
- **Multiple Download Modes**  
  - Single Video / MP3  
  - Playlist Video / Playlist MP3  
  - Channel Videos / Channel MP3  
  - Channel Shorts / Shorts MP3
- **Cookie‑Based Login**  
  Import YouTube cookies via “Get cookies.txt Locally” extension for authenticated downloads.
- **Modern PyQt6 GUI**  
  Intuitive sidebar, real‑time status, and scrolling activity log.
- **Flexible Quality Options**  
  Choose best‑available or specific resolutions (8K, 4K, 1080p, etc.); MP3 defaults to 320 kbps.
- **Lightweight & Cross‑Platform**  
  Single‑file app plus assets; runs on Windows, macOS, and Linux (ffmpeg required).

---

## 📁 Folder Structure

```
yt-downloader-gui/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── workflows/
│       └── python-publish.yml
├── .gitignore
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── pyproject.toml
├── requirements.txt
├── screenshots/
│   └── screenshot.png
├── src/
│   ├── build.bat
│   ├── favicon.ico
│   ├── main.py
│   ├── assets/
│   │   ├── activity.png
│   │   ├── download.png
│   │   ├── style.qss
│   │   └── video-favicon.png
│   ├── bin/
│   │   ├── ffmpeg.exe
│   │   └── yt-dlp.exe
│   └── app/
│       ├── __init__.py
│       ├── download_manager.py
│       ├── login_manager.py
│       ├── main_window.py
│       ├── ui_manager.py
│       └── updater.py
└── tests/
    ├── __init__.py
    ├── test_download_manager.py
    └── test_updater.py
```

---

## 📦 Requirements

- Python 3.8+  
- PyQt6  
- ffmpeg (bundled on Windows in `bin/ffmpeg.exe`; install separately on macOS/Linux)  
- yt-dlp (managed by the updater)

```bash
pip install -r requirements.txt
````

---

## 🚀 Installation

1. **Clone the repo:**

   ```bash
   git clone https://github.com/uikraft-hub/yt-downloader-gui.git
   cd yt-downloader-gui
   ```
2. **(Optional) Create & activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```
4. **Verify executables:**
   Ensure `bin/ffmpeg.exe` and `bin/yt-dlp.exe` exist. The app will update `yt-dlp.exe` on first run.

---

## ▶️ Usage

1. **Run the app:**

   ```bash
   python src/main.py
   ```
2. **Login with Cookies (for age‑restricted or region‑locked content):**

   * Go to **File → Login**, select your browser.
   * If you haven’t installed the “Get cookies.txt Locally” extension, the app will prompt you to do so.
   * Export your cookies, select the `.txt` file, then complete browser login.
3. **Download Workflow:**

   * Switch to **Download** page.
   * Paste a YouTube URL (video/playlist/channel/short).
   * Choose save location, download mode, and quality.
   * Click **Download** to queue.
4. **Monitor Progress:**

   * Switch to **Activity** page for real‑time logs and status.

---

## 🖼️ Screenshot

![Interface](screenshots/screenshot.png)

---

## 🤝 Contributing

We welcome contributions!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/awesome-thing`
3. Commit your changes with clear messages
4. Push to your fork and open a Pull Request

For major changes, please open an issue first to discuss.

---

## 🙏 Acknowledgments

* **yt-dlp** for the robust download backend
* **PyQt6** for the modern GUI framework
* **ffmpeg** for audio/video processing
* **GitHub API** for seamless updater integration

## 📞 Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/uikraft-hub/yt-downloader-gui/issues)
- **Discussions**: [Community discussions and Q&A](https://github.com/uikraft-hub/yt-downloader-gui/discussions)
- **Email**: ujjwalkrai@gmail.com

---

<div align="center">

**Made with ❤️ by the Ujjwal Nova**

[⭐ Star this repo](https://github.com/uikraft-hub/yt-downloader-gui) | [🐛 Report Bug](https://github.com/uikraft-hub/yt-downloader-gui/issues) | [💡 Request Feature](https://github.com/uikraft-hub/yt-downloader-gui/issues)

</div>
