# SSTube

[![Status](https://img.shields.io/badge/status-active-47c219.svg)](#) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

<p align="center">
  <img src="assets/Favicon.png" width="120" height="120" alt="SSTube Icon" />
</p>

**SSTube** is a powerful, open-source YouTube downloader application built with **PyQt6**. It supports multiple download modes (single videos, playlists, channels, shorts) and can also extract MP3 audio. With built-in browser login functionality, you can authenticate to YouTube and bypass certain restrictions (e.g., age-restricted content).

---

## Features

- **Multiple Download Modes**
  - **Single Video / MP3 Only**  
    Download a single YouTube video or extract audio as MP3.
  - **Playlist Video / Playlist MP3**  
    Download an entire playlist, with the option to pick specific videos.
  - **Channel Videos / Channel Videos MP3**  
    Download videos or MP3s from an entire YouTube channel.
  - **Channel Shorts / Channel Shorts MP3**  
    Focus on channel “Shorts” only, either in video or MP3 format.

- **Browser Login Support**  
  - Detects installed browsers on Windows and opens the YouTube login page in your selected browser.
  - After logging in, cookies are automatically used by **yt-dlp** to access restricted content.

- **Modern PyQt6 Interface**  
  - Intuitive layout with sidebar navigation.
  - Real-time status bar and activity log.

- **Flexible Quality Options**  
  - Choose from “Best Available” or specific resolutions for video (8K, 4K, 1080p, etc.).
  - MP3 downloads default to best-quality audio (320 kbps).

- **Lightweight & Easy to Use**  
  - Single-file application (`SSTube.py`) plus some assets/icons.
  - Minimal external dependencies.

---

## Folder Structure

```
SSTube/
├── SSTube.py
├── LICENSE
├── README.md
├── requirements.txt
├── .gitignore
├── assets/
│   ├── Favicon.png
│   ├── download.png
│   ├── activity.png
│   └── video-favicon.png
├── bin/
│   └── ffmpeg.exe
└── screenshots/
    └── (optional images or screenshots)
```

- **SSTube.py** — Main application code (PyQt6 + yt-dlp logic).  
- **requirements.txt** — Python dependencies.  
- **assets/** — Icons and images for the GUI.  
- **bin/** — Contains `ffmpeg.exe` (required for merging audio/video).  
- **screenshots/** — Optional folder for images in your documentation.

---

## Requirements

- [Python 3.8+](https://www.python.org/downloads/)  
- [ffmpeg](https://ffmpeg.org/) (already included in `bin/ffmpeg.exe` on Windows)  
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)  
- [PyQt6](https://pypi.org/project/PyQt6/)  

*(All dependencies should be installed via `pip install -r requirements.txt`.)*

---

## Installation

1. **Clone or Download** this repository:
   ```bash
   git clone https://github.com/yourusername/SSTube.git
   cd SSTube
   ```

2. **(Optional) Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Check ffmpeg**:
   - Ensure `bin/ffmpeg.exe` is present and accessible. If you’re on another platform, you may need to adjust the path or install ffmpeg separately.

---

## Usage

1. **Run the Application**:
   ```bash
   python SSTube.py
   ```
   A GUI window will appear.

2. **Login (Optional)**:
   - Click **File > Login** in the menu bar.
   - A dialog will list installed browsers (on Windows). Select one.
   - Your chosen browser will open the YouTube login page.
   - After logging in, return to SSTube and confirm. The cookies are now used by yt-dlp for restricted content.

3. **Download Workflow**:
   1. **Select “Download”** from the left sidebar.  
   2. **Enter the YouTube URL** (video, playlist, channel, or shorts).  
   3. **Select “Save Location”** to choose your download folder.  
   4. **Choose “Download Mode”** (Single Video, MP3 Only, Playlist, etc.).  
   5. For video modes, select your **Video Quality** (e.g., Best Available, 1080p, etc.).  
   6. **Click “Download”** to add the task to the queue.  

4. **Activity Log**:
   - Click “Activity” on the left sidebar to see real-time logs and download progress.

---

## Screenshots

<p align="center">
  <img src="screenshots/GUI.png" width="600" height="400" alt="Screenshots" />
</p>

---

## Contributing

Contributions are welcome! Here’s how you can help:

1. **Fork** the project on GitHub.  
2. **Create a feature branch** (e.g., `feature/new-mode`).  
3. **Commit** your changes.  
4. **Open a Pull Request** with a clear description of your additions.

For major changes, please open an issue first to discuss what you would like to change.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **yt-dlp** for the powerful downloading backend.  
- **PyQt6** for the GUI framework.  
- **ffmpeg** for audio/video processing.  
- Thanks to all contributors and testers!

---

**Enjoy using SSTube!** If you encounter any issues or have suggestions, please open an issue or submit a pull request. 
