# Usage Guide

A comprehensive guide on how to use the yt-downloader-gui - a PyQt6-based desktop app to download videos and audio from YouTube quickly and reliably.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [User Interface Guide](#user-interface-guide)
- [Supported URL Types](#supported-url-types)
- [Download Options](#download-options)
- [Advanced Settings](#advanced-settings)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)
- [API Reference](#api-reference)
- [FAQ](#faq)

## Overview

The yt-downloader-gui is a professional-grade tool designed to download media content from YouTube efficiently. Built with PyQt6, it provides an intuitive desktop interface for:

- **Media Extraction**: Download videos and audio from YouTube URLs.
- **Batch Processing**: Download multiple files from playlists and channels.
- **Format Support**: Download videos in MP4 format and audio in MP3 format.
- **Flexible Output**: Save files to a selected directory.
- **Quality Control**: Choose from various video quality options.
- **Professional UI**: Clean interface with real-time progress and logging.

## Quick Start

### Prerequisites

- Python 3.7 or higher
- Internet connection

### Installation

#### Method 1: Clone from GitHub

```bash
# Clone the repository
git clone https://github.com/uikraft-hub/yt-downloader-gui.git

# Navigate to the project directory
cd yt-downloader-gui

# Install required dependencies
pip install -r requirements.txt
```

## User Interface Guide

### Main Interface Components

#### 1. Header Section
- **Application Title**: yt-downloader-gui

#### 2. URL Input Section
- **YouTube URL Field**: Enter any valid YouTube URL.

#### 3. Settings Sidebar
- **Download Mode**: Select from various download modes.
- **Video Quality**: Choose the desired video quality.

#### 4. Download Section
- **Save Location**: Select the folder to save downloads.
- **Download Button**: Start the download process.

## Supported URL Types

### YouTube Video URLs
```
https://www.youtube.com/watch?v=...
```

### Playlist URLs
```
https://www.youtube.com/playlist?list=...
```

### Channel URLs
```
https://www.youtube.com/c/channelname
https://www.youtube.com/user/username
https://www.youtube.com/@handle
```

## Download Options

### Download Modes
- Single Video
- MP3 Only
- Playlist Video
- Playlist MP3
- Channel Videos
- Channel Videos MP3
- Channel Shorts
- Channel Shorts MP3

### Video Quality
- Best Available
- 4320p 8K
- 2160p 4K
- 1440p 2K
- 1080p Full HD
- 720p HD
- 480p Standard
- 360p Medium

## Advanced Settings

### Cookie-Based Login
For downloading age-restricted or private content, you can use cookie-based login.
1. Go to `File > Login`.
2. Select your browser.
3. Install the "Get cookies.txt Locally" extension if you haven't already.
4. Select the exported `cookies.txt` file.

## Running the Application 

### Basic Download Process

1. **Start the Application**
   ```bash
   python src/main.py
   ```

2. **Enter YouTube URL**
   - Paste any valid YouTube URL in the input field.

3. **Configure Download**
   - Select the download mode and video quality.
   - Choose a save location.

4. **Start Download**
   - Click the "Download" button.
   - Monitor progress in the "Activity" tab.

## Troubleshooting

### Common Issues and Solutions

#### "Download failed"
**Possible Causes:**
- Private or restricted YouTube content.
- Invalid or expired URL.
- Network connectivity issues.

**Solutions:**
1. Verify the YouTube URL is publicly accessible.
2. Try using cookie-based login for private content.
3. Check your internet connection.

## Best Practices

### Ethical Usage
- Respect YouTube's Terms of Service.
- Only download content you have permission to use.
- Consider copyright and intellectual property rights.

## API Reference

### Core Classes

#### YTDGUI
Main class for the GUI application.

#### DownloadManager
Handles the download queue and execution.

#### LoginManager
Handles user login and cookie-based authentication.

#### UIManager
Handles creation and management of the UI.

#### Updater
Handles automatic updates for the yt-dlp binary.

## FAQ

### General Questions

**Q: Is this application free to use?**
A: Yes, this is an open-source project under the MIT license.

**Q: Do I need a YouTube account?**
A: No, the application works with publicly accessible YouTube content. For private content, you can use cookie-based login.

**Q: Can I download private YouTube videos?**
A: Yes, by using the cookie-based login feature.

### Technical Questions

**Q: Why is my download slow?**
A: Download speed depends on your internet connection and the video quality selected.

**Q: Where are downloaded files saved?**
A: Files are saved in the directory you select.

## 📞 Support

- **📧 Email**: [ujjwalkrai@gmail.com](mailto:ujjwalkrai@gmail.com)
- **🐛 Issues**: [Repository Issues](https://github.com/uikraft-hub/yt-downloader-gui/issues)
- **🔓 Security**: [Repository Security](https://github.com/uikraft-hub/yt-downloader-gui/security)
- **⛏ Pull Requests**: [Repository Pull Requests](https://github.com/uikraft-hub/yt-downloader-gui/pulls)
- **📖 Documentation**: [Repository Documentation](https://github.com/uikraft-hub/yt-downloader-gui/tree/main/docs)
