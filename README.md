# SSTube v2.0

[![Status](https://img.shields.io/badge/status-active-47c219.svg)](#) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

<p align="center">
  <img src="assets/Favicon.png" width="120" height="120" alt="SSTube Icon" />
</p>

**SSTube** is a powerful, open-source YouTube downloader application built with **PyQt6** and **yt-dlp**. This release (v2.0) introduces enhanced cookie handling through a browser extension, multiple download modes (videos, playlists, channels, shorts, and MP3 extraction), and a refined user interface.

---

## Features

- **Multiple Download Modes**
  - **Single Video / MP3 Only**  
    Download a single YouTube video or extract its audio as MP3.
  - **Playlist Video / Playlist MP3**  
    Download an entire playlist with an option to select specific videos.
  - **Channel Videos / Channel Videos MP3**  
    Download all videos (or extract audio) from a YouTube channel.
  - **Channel Shorts / Channel Shorts MP3**  
    Focus on downloading YouTube Shorts.

- **Cookie Extension Support**
  - **Secure Cookie File Import:**  
    Instead of automatic browser cookie extraction, SSTube now relies on a cookie file exported by the **"Get cookies.txt Locally"** extension.
  - **Guided Workflow:**  
    If the extension isn’t installed, SSTube will automatically open the extension’s page in your selected browser, then prompt you to export and select your YouTube cookie file.
  - **Validation:**  
    SSTube verifies that the selected cookie file contains YouTube cookies to ensure proper authentication.

- **Modern PyQt6 Interface**
  - Intuitive sidebar navigation for quick access to Download and Activity pages.
  - Real-time status updates and activity logs.

- **Flexible Quality Options**
  - Choose from “Best Available” or specific resolutions (8K, 4K, 1080p, etc.) for video downloads.
  - MP3 extraction defaults to 320 kbps audio quality.

- **Lightweight & Easy to Use**
  - Single-file application (`SSTube.py`) plus a few assets.
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

- **SSTube.py** — Main application code (PyQt6 & yt-dlp logic).
- **requirements.txt** — Python dependencies.
- **assets/** — Icons and images for the GUI.
- **bin/** — Contains `ffmpeg.exe` (required for merging audio/video streams).
- **screenshots/** — Optional folder for screenshots and additional images.

---

## Requirements

- [Python 3.8+](https://www.python.org/downloads/)
- [ffmpeg](https://ffmpeg.org/) (already included in `bin/ffmpeg.exe` on Windows)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [PyQt6](https://pypi.org/project/PyQt6/)

*(Install all dependencies via `pip install -r requirements.txt`.)*

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
   source venv/bin/activate      # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure ffmpeg is Accessible**:
   - Confirm that `bin/ffmpeg.exe` exists. If you're on another platform, adjust the path or install ffmpeg separately.

---

## Usage

1. **Run the Application**:
   ```bash
   python SSTube.py
   ```
   The SSTube GUI will open.

2. **Cookie Login Feature**
   - Click **File > Login** from the menu bar.
   - A dialog will prompt you to select the browser you use for YouTube login.
   - You will then be asked if you have installed the **"Get cookies.txt Locally"** extension.
     - **If Yes:**  
       You’ll be prompted to select the exported cookie file. SSTube validates the file to ensure it contains YouTube cookies.
     - **If No:**  
       The extension’s page will be opened in your selected browser so you can install it. After installing, export your cookies and then select the exported cookie file.
   - Once a valid cookie file is selected, SSTube uses it for authentication and access to restricted YouTube content.
   
3. **Download Workflow**
   - Go to the **Download** page via the sidebar.
   - Enter the YouTube URL (video, playlist, channel, or shorts).
   - Select a save location for the downloads.
   - Choose the appropriate **Download Mode** and, if applicable, set the video quality.
   - Click **Download** to add the task to the queue.
   
4. **Activity Log**
   - Use the **Activity** page to monitor real-time logs and download progress.

---

## Screenshots

*(Optional – include images from the `screenshots/` folder if desired.)*

<p align="center">
  <img src="screenshots/GUI.png" width="600" height="400" alt="SSTube GUI" />
</p>


---

## Building the Executable

You can use [PyInstaller](https://www.pyinstaller.org/) to package SSTube as a standalone executable. For example:

```bash
pyinstaller --onefile --windowed --icon "assets/Favicon.png" --add-data "assets;assets" --add-data "bin;bin" SSTube.py
```

This command creates a single executable (`SSTube.exe`) in the `dist/` folder.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the project on GitHub.
2. **Create a new branch** (e.g., `feature/new-feature`).
3. **Commit** your changes with clear messages.
4. **Submit a Pull Request** with a detailed description of your changes.

For major changes, please open an issue first to discuss what you would like to change.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **yt-dlp** for the robust downloading backend.
- **PyQt6** for the powerful GUI framework.
- **ffmpeg** for multimedia processing.
- Thanks to all the contributors and testers!

---

**Enjoy using SSTube!** If you encounter any issues or have suggestions, please open an issue or submit a pull request.
```

This README.md provides a complete overview of SSTube v2.1.0 with detailed instructions on using the cookie extension feature, installation, usage, building, and contribution guidelines.