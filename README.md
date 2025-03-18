# SSTube

[![Status](https://img.shields.io/badge/status-active-47c219.svg)](https://github.com/UKR-PROJECTS/SSTube)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

<p align="center">
  <img src="assets/Favicon.png" width="300" height="300" alt="SSTube Icon" />
</p>

SSTube is a powerful, open-source YouTube downloader application built with **PyQt6**. It supports multiple download modes—including single videos, playlists, channels (both videos and shorts), and MP3 extractions—making it easy to save your favorite content in the format you want.

## Features

- **Multiple Download Modes:**
  - **Single Video / MP3 Only:** Download a single YouTube video or extract audio as MP3.
  - **Playlist Video / Playlist MP3:** Download an entire playlist, with an option to select specific videos.
  - **Channel Videos / Channel Videos MP3:** Download videos from a YouTube channel.
  - **Channel Shorts / Channel Shorts MP3:** Download only the shorts from a channel.
- **Modern, Professional GUI:**  
  Built with PyQt6 for a responsive and user-friendly interface.
- **Real-Time Activity Log:**  
  Monitor download progress and view status messages.
- **Integrated ffmpeg:**  
  Uses an external ffmpeg binary (included in the `bin/` folder) to merge audio and video streams.

## Folder Structure
- **README.md:** Project overview, instructions, and documentation.
- **LICENSE:** The project's license (MIT License).
- **requirements.txt:** List of Python dependencies.
- **.gitignore:** Files and folders to be excluded from Git version control.
- **SSTube.py:** The single source file containing the entire application.
- **assets/:** Contains images and icons used by the application.
- **bin/:** Contains external binaries (e.g., `ffmpeg.exe`).

## Getting Started

### Prerequisites

- [Python 3.8+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/SSTube.git
   cd SSTube
   ```

2. **Set Up a Virtual Environment (Recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

### Running SSTube

Simply run the main script:

```bash
python SSTube.py
```

The application window will open, allowing you to enter a YouTube URL (or Playlist/Channel URL) and select the desired download mode. For video modes, you can select the video quality; for MP3 modes, the best available audio is automatically used.

## Usage

1. **Download Page:**  
   - Enter the URL of the video, playlist, or channel.
   - Select the download mode from the dropdown menu.
   - For video downloads, choose your desired quality.
   - Click the **Download** button to add the task to the queue.

2. **Activity Page:**  
   - Monitor real-time progress and status messages as downloads are processed.
  
3. **Assets & Binaries:**  
   - Make sure that the `assets/` folder contains the necessary icons.
   - The `bin/` folder must include `ffmpeg.exe` for proper video/audio merging.

## Contributing

Contributions are welcome! Follow these steps to contribute:

1. **Fork the Repository:**  
   Click the **Fork** button on the GitHub page.

2. **Clone Your Fork:**

   ```bash
   git clone https://github.com/yourusername/SSTube.git
   cd SSTube
   ```

3. **Create a New Branch:**

   ```bash
   git checkout -b feature/YourFeatureName
   ```

4. **Make Your Changes:**  
   Ensure your code is well-documented and tested.

5. **Submit a Pull Request:**  
   Push your branch and open a pull request with a detailed description of your changes.

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for video downloading.
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/intro) for the GUI framework.
- Community contributions and support.

---


```
If you encounter any issues, please use GitHub Issues to report them. Enjoy using SSTube!

