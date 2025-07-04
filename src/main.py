"""
Youtube-Media-Downloader - Professional YouTube Video Downloader
==============================================

A PyQt6-based GUI application for downloading YouTube videos, playlists, and channels.
Supports both video and audio-only downloads with customizable quality settings.

Author: Ujjwal Nova
Version: 2.3.1
License: MIT
Repository: https://github.com/ukr-projects/yt-downloader-gui

Features:
- Single video and playlist downloads
- Channel video and shorts downloads
- MP3 audio extraction
- Cookie-based authentication for private content
- Automatic yt-dlp updates
- Multi-threaded downloading
- Progress tracking and logging

Dependencies:
- PyQt6: GUI framework
- yt-dlp: YouTube downloading engine
- FFmpeg: Audio/video processing (external binary)

Usage:
    cd src
    python main.py
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from app.main_window import YTDGUI


def main():
    """
    Main application entry point.

    Initializes the Qt application and starts the main event loop.
    """
    # Create Qt application
    app = QApplication(sys.argv)

    # Set application metadata
    app.setApplicationName("yt-downloader")
    app.setApplicationVersion("2.3.1")

    # Determine application base directory
    if getattr(sys, "frozen", False):
        # Running as compiled executable
        base_dir = os.path.dirname(sys.executable)
    else:
        # Running as Python script
        base_dir = os.path.dirname(os.path.abspath(__file__))

    # Create and show main window
    window = YTDGUI(base_dir)
    window.show()

    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
