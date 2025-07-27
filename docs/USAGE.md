# Usage Guide

A comprehensive guide on how to use the Pinterest Media Scraper - a Streamlit-based desktop/web app to download images and videos from Pinterest pins, boards, and profiles quickly and reliably.

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

The Pinterest Media Scraper is a professional-grade tool designed to download media content from Pinterest efficiently. Built with Streamlit, it provides an intuitive web interface for:

- **Media Extraction**: Download images and videos from Pinterest pins, boards, and profiles
- **Batch Processing**: Download multiple files simultaneously with progress tracking
- **Format Support**: Handle JPG, PNG, GIF, WebP images and MP4, WebM videos
- **Flexible Output**: Save as individual files or bundled ZIP archives
- **Quality Control**: Advanced settings for timeout, retries, and concurrency
- **Professional UI**: Clean interface with real-time previews and metrics

## Quick Start

### Prerequisites

- Python 3.7 or higher
- Internet connection
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

#### Method 1: Clone from GitHub

```bash
# Clone the repository
git clone https://github.com/uikraft-hub/pinterest-media-scraper.git

# Navigate to the project directory
cd pinterest-media-scraper

# Install required dependencies
pip install -r requirements.txt
```

The application will automatically open in your default web browser at `http://localhost:8501`

## User Interface Guide

### Main Interface Components

#### 1. Header Section
- **Application Title**: Pinterest Media Downloader
- **Description**: Professional tool introduction

#### 2. URL Input Section
- **Pinterest URL Field**: Enter any valid Pinterest URL
- **Analyze Button**: Process the URL to find downloadable media
- **Real-time Validation**: Instant feedback on URL validity

#### 3. Settings Sidebar
- **Download Quality**: High, Medium, Low options
- **Output Format**: Original files or ZIP archive
- **Advanced Settings**: Timeout, retries, concurrent downloads

#### 4. Media Info Panel
- **Total Media Count**: Number of files found
- **Media Previews**: Thumbnail previews of first 3 items
- **File Type Breakdown**: Images vs. videos count

#### 5. Download Section
- **File Count Selection**: Choose how many files to download
- **Quick Select Buttons**: First 5, First 10, All Files
- **Progress Tracking**: Real-time download progress
- **Download Buttons**: Individual files or ZIP archive

## Supported URL Types

### Pinterest Pin URLs
```
https://www.pinterest.com/pin/123456789/
https://pinterest.com/pin/123456789/
https://in.pinterest.com/pin/123456789/
```

### Short URLs
```
https://pin.it/abc123
```

### Board URLs
```
https://www.pinterest.com/username/board-name/
```

### Profile URLs
```
https://www.pinterest.com/username/
```

### Search URLs
```
https://www.pinterest.com/search/pins/?q=search-term
```

## Download Options

### File Count Selection

#### Manual Selection
Use the number input field to specify exactly how many files to download (1 to total available).

#### Quick Select Options
- **First 5**: Download the first 5 media files
- **First 10**: Download the first 10 media files
- **All Files**: Download all available media files

### Output Formats

#### Original Files
- Downloads each file individually
- Preserves original file names and formats
- Allows selective downloading of specific files

#### ZIP Archive
- Bundles all selected files into a single ZIP file
- Convenient for bulk downloads
- Automatically named `pinterest_media.zip`

### File Naming Convention
```
pinterest_media_001.jpg
pinterest_media_002.png
pinterest_media_003.mp4
...
```

## Advanced Settings

### Quality Settings
- **High**: Original resolution images and videos
- **Medium**: Balanced quality and file size
- **Low**: Compressed versions for faster downloads

### Network Settings

#### Request Timeout
- **Range**: 5-60 seconds
- **Default**: 30 seconds
- **Purpose**: Maximum time to wait for server response

#### Max Retries
- **Range**: 1-5 attempts
- **Default**: 3 attempts
- **Purpose**: Number of retry attempts for failed downloads

#### Concurrent Downloads
- **Range**: 1-10 simultaneous downloads
- **Default**: 3 concurrent downloads
- **Purpose**: Balance between speed and server load

## Running the Application 

### Basic Download Process

1. **Start the Application**
   ```bash
   streamlit run main.py
   ```

2. **Enter Pinterest URL**
   - Paste any valid Pinterest URL in the input field
   - The system will validate the URL in real-time

3. **Analyze the URL**
   - Click the "🔍 Analyze URL" button
   - Wait for the system to scan and extract media URLs
   - Review the found media count and preview

4. **Configure Download**
   - Select the number of files to download
   - Choose output format (Original or ZIP)
   - Adjust settings in the sidebar if needed

5. **Start Download**
   - Click "🚀 Start Download" button
   - Monitor progress in real-time
   - Download completed files or ZIP archive

### Advanced Usage

#### Batch Processing Multiple URLs
1. Process first URL and download
2. Clear the URL field
3. Enter next URL and repeat
4. Files are saved separately for each URL

#### Custom Quality Settings
1. Open sidebar settings
2. Select desired quality level
3. Adjust timeout and retry settings for unstable connections
4. Set appropriate concurrent downloads for your internet speed

## Troubleshooting

### Common Issues and Solutions

#### "No media files found"
**Possible Causes:**
- Private or restricted Pinterest content
- Invalid or expired URL
- Pinterest's anti-scraping measures
- Network connectivity issues

**Solutions:**
1. Verify the Pinterest URL is publicly accessible
2. Try using a pin.it short URL instead
3. Check if the pin still exists on Pinterest
4. Try a different Pinterest URL
5. Wait a few minutes and try again
6. For search URLs, try individual pin URLs instead

#### "Invalid Pinterest URL"
**Possible Causes:**
- Incorrect URL format
- Non-Pinterest URL entered
- URL contains invalid characters

**Solutions:**
1. Ensure URL starts with `https://`
2. Verify it's a Pinterest domain (pinterest.com, pin.it)
3. Copy URL directly from Pinterest
4. Remove any extra parameters or fragments

#### Download Failures
**Possible Causes:**
- Network interruption
- Server-side blocks
- File size limitations
- Permission issues

**Solutions:**
1. Increase timeout in advanced settings
2. Reduce concurrent downloads
3. Try downloading fewer files at once
4. Check internet connection stability
5. Restart the application

#### Slow Download Speeds
**Solutions:**
1. Reduce concurrent downloads to 1-2
2. Increase timeout setting
3. Choose lower quality setting
4. Download during off-peak hours

### Error Messages

#### Connection Timeout
```
Error: Request timed out after 30 seconds
```
**Solution**: Increase timeout in advanced settings

#### Too Many Requests
```
Error: Rate limited by Pinterest
```
**Solution**: Wait 5-10 minutes before trying again

#### Invalid File Format
```
Error: Unsupported file format
```
**Solution**: Check if Pinterest changed their media format

## Best Practices

### Ethical Usage
- Respect Pinterest's Terms of Service
- Only download content you have permission to use
- Consider copyright and intellectual property rights
- Don't overload Pinterest's servers with excessive requests

### Performance Optimization
- Start with small batches (5-10 files) to test
- Use appropriate concurrent download settings
- Monitor your internet bandwidth usage
- Clear browser cache if experiencing issues

### File Management
- Organize downloads in separate folders by project
- Use descriptive folder names for different Pinterest boards
- Regularly clean up temporary files
- Keep backups of important downloaded content

### Security Considerations
- Keep the application updated
- Don't share downloaded content without permission
- Be aware of privacy implications when downloading user content
- Use the application on trusted networks

## API Reference

### Core Classes

#### PinterestDownloader
Main class handling media extraction and downloading.

```python
from app.downloader import PinterestDownloader

downloader = PinterestDownloader()
```

**Methods:**
- `get_media_info(url)`: Extract media URLs from Pinterest page
- `download_media(urls, output_dir, max_files, progress_callback)`: Download media files
- `create_zip(files, zip_path)`: Create ZIP archive from files

#### Utility Functions

```python
from app.utils import validate_pinterest_url, normalize_pinterest_url

# Validate URL format
is_valid = validate_pinterest_url(url)

# Normalize URL for processing
normalized_urls = normalize_pinterest_url(session, url)
```

### Configuration Options

#### Session Headers
The downloader uses realistic browser headers to avoid detection:
- User-Agent: Chrome browser simulation
- Accept: Standard web content types
- Connection: Keep-alive for efficiency

#### URL Processing
- Automatic short URL resolution (pin.it → pinterest.com)
- Country-specific domain normalization
- Pin ID extraction for direct access

## FAQ

### General Questions

**Q: Is this application free to use?**
A: Yes, this is an open-source project under MIT license.

**Q: Do I need a Pinterest account?**
A: No, the application works with publicly accessible Pinterest content.

**Q: Can I download private Pinterest boards?**
A: No, only publicly accessible content can be downloaded.

**Q: What file formats are supported?**
A: Images: JPG, PNG, GIF, WebP | Videos: MP4, WebM, MOV

### Technical Questions

**Q: Why is my download slow?**
A: Reduce concurrent downloads, increase timeout, or check your internet connection.

**Q: Can I pause and resume downloads?**
A: Currently, downloads cannot be paused. You can stop and restart the application.

**Q: Where are downloaded files saved?**
A: Files are temporarily processed and offered for browser download. Check your browser's download folder.

**Q: Can I change the output file names?**
A: Currently, files use automatic naming. Manual renaming must be done after download.

### Troubleshooting Questions

**Q: The application won't start. What should I do?**
A: Ensure Python 3.7+ is installed and all dependencies are installed via `pip install -r requirements.txt`.

**Q: I get "No media found" for a valid Pinterest URL. Why?**
A: This could be due to Pinterest's protection measures, private content, or temporary server issues. Try again later or with a different URL.

**Q: Can I download entire Pinterest boards at once?**
A: The application processes URLs and finds available media. For boards, it will attempt to find all accessible pins.

## 📞 Support

- **📧 Email**: [ujjwalkrai@gmail.com](mailto:ujjwalkrai@gmail.com)
- **🐛 Issues**: [Repository Issues](https://github.com/uikraft-hub/pinterest-media-scraper/issues)
- **🔓 Security**: [Repository Security](https://github.com/uikraft-hub/pinterest-media-scraper/security)
- **⛏ Pull Requests**: [Repository Pull Requests](https://github.com/uikraft-hub/pinterest-media-scraper/pulls)
- **📖 Documentation**: [Repository Documentation](https://github.com/uikraft-hub/pinterest-media-scraper/tree/main/docs)

### Contributing

If you encounter bugs or have feature requests:

1. Check [existing issues](https://github.com/uikraft-hub/pinterest-media-scraper/issues)
2. Create a new issue with detailed description
3. Follow the [Contributing Guidelines](https://github.com/uikraft-hub/pinterest-media-scraper/blob/main/docs/CONTRIBUTING.md)
4. Submit pull requests for improvements

### Community

Join our community of users and contributors:
- Star the repository if you find it useful
- Share with others who might benefit
- Contribute improvements and bug fixes
- Provide feedback and suggestions

---

**Made with ❤️ for the Pinterest community**

*This tool helps users efficiently download Pinterest media while respecting platform policies and user rights.*
