# SSTube v2.2.0

[![Status](https://img.shields.io/badge/status-active-47c219.svg)](#) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

<p align="center">
  <img src="src/assets/video-favicon.png" width="120" height="120" alt="SSTube Icon" />
</p>

**SSTube** is a powerful, open-source YouTube downloader application built with **PyQt6** and **yt-dlp**. Version **2.2.0** brings you an **automatic updater** for yt-dlp, so you’re always running the latest downloader backend, plus all the familiar download modes and cookie-based authentication you love.

---

## Features

- **Automatic yt-dlp Updater**  
  - **GitHub Release Check**  
    On startup, SSTube will ask if you’d like to check for a new yt-dlp release on GitHub.  
  - **Seamless Download & Replace**  
    Fetches the latest `yt-dlp.exe`, replaces your existing copy, and makes it executable—no manual steps required.

- **Multiple Download Modes**  
  - **Single Video / MP3 Only**  
    Download a single YouTube video or extract its audio as MP3.  
  - **Playlist Video / Playlist MP3**  
    Download an entire playlist with the option to include only selected videos.  
  - **Channel Videos / Channel Videos MP3**  
    Download all videos (or just their audio) from a YouTube channel.  
  - **Channel Shorts / Channel Shorts MP3**  
    Focus exclusively on downloading YouTube Shorts content.

- **Cookie Extension Support**  
  - **Secure Cookie File Import**  
    SSTube uses a cookie file exported by the **“Get cookies.txt Locally”** extension for authentication.  
  - **Guided Workflow**  
    If the extension isn’t installed, SSTube opens its store page in your chosen browser and guides you through export and selection.  
  - **Validation**  
    Ensures the selected cookie file actually contains YouTube cookies before proceeding.

- **Modern PyQt6 Interface**  
  - Intuitive sidebar navigation between **Download** and **Activity** pages.  
  - Real-time status updates and a scrolling activity log.

- **Flexible Quality Options**  
  - Choose **Best Available** or specific resolutions (8K, 4K, 1080p, etc.) for video.  
  - MP3 extraction defaults to **320 kbps** audio quality.

- **Lightweight & Easy to Use**  
  - Single-file application (`SSTube.py`) plus a small assets folder.  
  - Minimal external dependencies; runs on Windows, macOS, and Linux (with locally installed `ffmpeg`).

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
│   ├── ffmpeg.exe
│   └── yt-dlp.exe       # Automatically updated by the Updater
└── screenshots/


````

- **SSTube.py** — Main application logic (PyQt6 GUI, yt-dlp integration, updater).  
- **requirements.txt** — Python dependencies list.  
- **assets/** — GUI icons and images.  
- **bin/** — Bundled `ffmpeg.exe` and `yt-dlp.exe`.  
- **screenshots/** — Add your own screenshots for documentation.

---

## Requirements

- **Python 3.8+**  
- **ffmpeg** (included in `bin/ffmpeg.exe` on Windows; install separately on other OS)  
- **yt-dlp** (managed automatically by SSTube’s updater)  
- **PyQt6**  

```bash
pip install -r requirements.txt
````

---

## Installation

1. **Clone or Download** this repository:

   ```bash
   git clone https://github.com/UKR-PROJECTS/SSTube.git
   cd SSTube
   ```

2. **(Optional) Create & Activate a Virtual Environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Verify `ffmpeg` & `yt-dlp`** exist in `bin/`. SSTube will update `yt-dlp.exe` automatically.

---

## Usage

1. **Run SSTube**:

   ```bash
   python SSTube.py
   ```

   * On first launch (and each subsequent startup), you’ll be prompted to **Check for Updates** to yt-dlp. Choosing **Yes** will download and install the latest `yt-dlp.exe`.

2. **Login with Cookies**

   * From **File > Login**, select your browser and indicate whether you’ve installed the **Get cookies.txt Locally** extension.
   * If needed, SSTube opens the extension page, then prompts you to select the exported cookie file.
   * After selecting a valid cookie file, SSTube opens YouTube’s login page in your browser—log in there, then return to SSTube.

3. **Download Workflow**

   * Navigate to the **Download** page.
   * Enter a YouTube URL (video, playlist, channel or shorts).
   * Choose a **Save Location**.
   * Select a **Download Mode** and, if applicable, a **Video Quality**.
   * Click **Download** to queue the task.

4. **Monitor Progress**

   * Switch to the **Activity** page to view real-time logs and download status.

---

## Screenshots

<p align="center">
  <img src="screenshots/GUI.png" width="600" height="400" alt="SSTube GUI" />
</p>


---

## Building a Standalone Executable

Use [PyInstaller](https://www.pyinstaller.org/):

```bash
pyinstaller --onefile --windowed --icon "assets/Favicon.png" --add-data "assets;assets" --add-data "bin;bin" SSTube.py
```

This creates `dist/SSTube.exe` (or the equivalent on your platform).

---

## Contributing

We welcome all contributions!

1. **Fork** the repository.
2. **Create a feature branch** (`git checkout -b feature/awesome-feature`).
3. **Commit** with clear, descriptive messages.
4. **Push** to your fork and **open a Pull Request**.

For major changes, please open an issue first to discuss.

---

## License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## Acknowledgments

* **yt-dlp** for the powerful download backend.
* **PyQt6** for the modern GUI framework.
* **ffmpeg** for multimedia processing.
* **GitHub API** for seamless updater integration.
* Thanks to all contributors and testers!

---

**Enjoy SSTube v2.2.0!** If you encounter any issues or have suggestions, please open an issue or submit a pull request.

