"""
SSTube - Professional YouTube Video Downloader
==============================================

A PyQt6-based GUI application for downloading YouTube videos, playlists, and channels.
Supports both video and audio-only downloads with customizable quality settings.

Author: Ujjwal Nova
Version: 2.2.0
License: MIT

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
    python SStube.py

Repository: https://github.com/UKR-PROJECTS/SSTube
"""

import os
import sys
import threading
import webbrowser
import json
import urllib.request
import shutil
import stat
import subprocess
import re
from typing import Dict, List, Optional, Callable, Tuple, Any

# Third-party imports
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class Updater:
    """
    Handles automatic updates for yt-dlp binary.

    This class manages checking for and downloading the latest version of yt-dlp
    from the official GitHub releases API.
    """

    # GitHub API endpoint for yt-dlp releases
    YTDLP_RELEASES = "https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest"

    def __init__(self, base_dir: str, parent: Optional[QWidget] = None):
        """
        Initialize the updater.

        Args:
            base_dir: Base directory where the application is installed
            parent: Parent widget for GUI operations
        """
        self.base_dir = base_dir
        self.parent = parent
        self.yt_dlp_path = os.path.join(base_dir, "bin", "yt-dlp.exe")

    def get_latest_yt_version(self) -> Tuple[str, List[Dict]]:
        """
        Fetch the latest yt-dlp version information from GitHub API.

        Returns:
            Tuple containing version string and list of release assets

        Raises:
            urllib.error.URLError: If API request fails
            json.JSONDecodeError: If response is not valid JSON
        """
        with urllib.request.urlopen(self.YTDLP_RELEASES) as resp:
            data = json.load(resp)

        version = data.get("tag_name", "").lstrip("release/")
        assets = data.get("assets", [])

        return version, assets

    def download_yt(self, progress_callback: Callable[[str], None]) -> None:
        """
        Download and install the latest yt-dlp executable.

        Args:
            progress_callback: Function to call with progress updates

        Raises:
            Exception: If download or installation fails
        """
        version, assets = self.get_latest_yt_version()

        # Find the executable asset in the release
        exe_asset = next((a for a in assets if a["name"].endswith(".exe")), None)
        if not exe_asset:
            progress_callback("No yt-dlp executable found in release assets.")
            return

        url = exe_asset["browser_download_url"]
        target = self.yt_dlp_path

        progress_callback(f"Downloading yt-dlp {version}...")

        # Download to temporary file first, then replace existing
        temp_path = target + ".new"
        try:
            with urllib.request.urlopen(url) as response, open(temp_path, "wb") as file:
                shutil.copyfileobj(response, file)

            # Atomically replace the old file
            os.replace(temp_path, target)

            # Set executable permissions (Unix-style, may not work on Windows)
            os.chmod(target, stat.S_IEXEC | stat.S_IREAD | stat.S_IWRITE)

            progress_callback(f"yt-dlp updated to {version} at {target}")

        except Exception as e:
            # Clean up temporary file if it exists
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise e


class SSTubeGUI(QMainWindow):
    """
    Main GUI application class for SSTube YouTube downloader.

    This class implements the complete user interface and handles all user interactions,
    download management, and application state.
    """

    # Custom signals for thread-safe GUI updates
    updateStatusSignal = pyqtSignal(str)
    logMessageSignal = pyqtSignal(str)

    def __init__(self):
        """Initialize the main application window and all components."""
        super().__init__()

        # Window configuration
        self.setWindowTitle("SSTube")
        self.resize(400, 300)

        # Determine application base directory (handles both script and frozen executable)
        if getattr(sys, "frozen", False):
            # Running as compiled executable
            self.base_dir = os.path.dirname(sys.executable)
        else:
            # Running as Python script
            self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # Initialize updater component
        self.updater = Updater(self.base_dir, parent=self)

        # Set application icon
        self._set_window_icon()

        # Initialize application state
        self._initialize_state()

        # Load UI icons
        self._load_icons()

        # Build user interface
        self._create_ui()

        # Connect signals for thread-safe updates
        self._connect_signals()

        # Initial status
        self.update_status("Ready")

        # Check for updates on startup (delayed to allow UI to render)
        QTimer.singleShot(100, self.check_for_updates)

    def _set_window_icon(self) -> None:
        """Set the application window icon if available."""
        try:
            icon_path = os.path.join(self.base_dir, "favicon.ico")
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))
        except Exception:
            # Silently continue if icon cannot be loaded
            pass

    def _initialize_state(self) -> None:
        """Initialize application state variables."""
        # Download management
        self.download_queue: List[Dict[str, Any]] = []
        self.downloading = False

        # Audio settings
        self.audio_quality_default = "320"

        # Authentication settings
        self.use_cookies = False
        self.cookie_browser = "chrome"
        self.cookie_file: Optional[str] = None

    def _load_icons(self) -> None:
        """Load application icons from assets directory."""
        self.icons = {
            "download": self.load_icon(os.path.join(self.base_dir, "assets", "download.png")),
            "activity": self.load_icon(os.path.join(self.base_dir, "assets", "activity.png")),
        }

        # Load video favicon for playlist/channel selection dialogs
        try:
            vf_path = os.path.join(self.base_dir, "assets", "video-favicon.png")
            if os.path.exists(vf_path):
                self.video_favicon_pixmap = (
                    QPixmap(vf_path)
                    .scaled(16, 16, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                )
            else:
                self.video_favicon_pixmap = None
        except Exception:
            self.video_favicon_pixmap = None

    def _create_ui(self) -> None:
        """Create and layout the main user interface."""
        # Create menu bar
        self.create_menubar()

        # Central widget with horizontal layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        # Sidebar navigation
        self.sidebar = self.create_sidebar()
        layout.addWidget(self.sidebar)

        # Main content area with stacked pages
        self.stack = QStackedWidget()
        self.download_page = self.create_download_page()
        self.activity_page = self.create_activity_page()
        self.stack.addWidget(self.download_page)
        self.stack.addWidget(self.activity_page)
        layout.addWidget(self.stack, 1)  # Expand to fill available space

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def _connect_signals(self) -> None:
        """Connect Qt signals for thread-safe GUI updates."""
        self.updateStatusSignal.connect(self._update_status)
        self.logMessageSignal.connect(self._log_message)

    def load_icon(self, path: str) -> QIcon:
        """
        Load an icon from the specified path.

        Args:
            path: File path to the icon image

        Returns:
            QIcon object (empty if loading fails)
        """
        try:
            if os.path.exists(path):
                return QIcon(QPixmap(path))
        except Exception:
            pass
        return QIcon()

    def create_menubar(self) -> None:
        """Create the application menu bar with File and Help menus."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        # Login action for cookie-based authentication
        login_action = QAction("Login", self)
        login_action.triggered.connect(self.open_login)
        file_menu.addAction(login_action)

        file_menu.addSeparator()

        # Exit action
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Help menu
        help_menu = menubar.addMenu("Help")

        # About dialog
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def check_for_updates(self) -> None:
        """
        Prompt user to check for yt-dlp updates on application startup.

        This runs automatically when the application starts and gives the user
        the option to update yt-dlp to the latest version.
        """
        reply = QMessageBox.question(
            self, "Check for Updates",
            "Do you want to check for a new version of yt-dlp?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Switch to activity page to show update progress
            self.switch_page("Activity")
            # Run update in background thread
            threading.Thread(target=self.run_updates, daemon=True).start()

    def run_updates(self) -> None:
        """
        Execute yt-dlp update process in background thread.

        This method runs in a separate thread to avoid blocking the UI
        during the update process.
        """

        def progress_callback(msg: str) -> None:
            """Callback function to report update progress."""
            self.log_message(msg)

        self.log_message("Starting yt-dlp update...")

        try:
            self.updater.download_yt(progress_callback)
            self.log_message("yt-dlp update completed successfully.")
        except Exception as e:
            error_msg = f"Update error: {e}"
            self.log_message(error_msg)

            # Show error dialog in main thread
            QTimer.singleShot(0, lambda: QMessageBox.critical(
                self, "Updater", f"Error during yt-dlp update: {e}"
            ))

    def get_installed_browsers(self) -> List[str]:
        """
        Get list of installed browsers on Windows system.

        Returns:
            List of browser names found in the Windows registry

        Note:
            Falls back to common browser names if registry access fails
        """
        try:
            import winreg

            # Access Windows registry for installed browsers
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Clients\StartMenuInternet"
            )

            browsers = []
            i = 0

            # Enumerate all browser entries
            while True:
                try:
                    browser_name = winreg.EnumKey(key, i)
                    browsers.append(browser_name)
                    i += 1
                except OSError:
                    # No more entries
                    break

            winreg.CloseKey(key)

            # Return found browsers or fallback list
            return browsers if browsers else self._get_fallback_browsers()

        except Exception:
            # Registry access failed, return common browsers
            return self._get_fallback_browsers()

    def _get_fallback_browsers(self) -> List[str]:
        """Get fallback list of common browsers."""
        return ["Google Chrome", "Mozilla Firefox", "Microsoft Edge"]

    def map_browser(self, browser_name: str) -> str:
        """
        Map browser display name to yt-dlp compatible browser identifier.

        Args:
            browser_name: Display name of the browser

        Returns:
            yt-dlp compatible browser identifier
        """
        name = browser_name.lower()

        # Map common browser names to yt-dlp identifiers
        browser_mapping = {
            "chrome": "chrome",
            "firefox": "firefox",
            "edge": "edge",
            "opera": "opera",
            "brave": "brave"
        }

        # Find matching browser
        for key, value in browser_mapping.items():
            if key in name:
                return value

        # Return original name if no mapping found
        return name

    def open_login(self) -> None:
        """
        Handle user login process for accessing private YouTube content.

        This method guides the user through setting up cookie-based authentication
        for downloading private or age-restricted content.
        """
        # Check if already logged in
        if self.use_cookies:
            QMessageBox.information(self, "Login", "Already logged in.")
            return

        # Get user's browser preference
        installed_browsers = self.get_installed_browsers()
        browser_choice, ok = QInputDialog.getItem(
            self, "Select Browser", "Select your browser:",
            installed_browsers, 0, False
        )

        if not ok:
            return

        self.cookie_browser = self.map_browser(browser_choice)

        # Check if user has cookie extension installed
        reply = QMessageBox.question(
            self,
            "Cookie Extension",
            "Have you installed the 'Get cookies.txt Locally' extension?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        # Browser executable paths for different browsers
        browser_paths = {
            "chrome": r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
            "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            "opera": r"C:\Program Files\Opera\launcher.exe",
            "brave": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        }

        exe_path = browser_paths.get(self.cookie_browser)

        if reply == QMessageBox.StandardButton.Yes:
            # User has extension, let them select cookie file
            self._handle_cookie_file_selection()
        else:
            # User doesn't have extension, guide them to install it
            self._guide_extension_installation(exe_path)

        # If login was successful, open YouTube login page
        if self.use_cookies:
            self._open_youtube_login(exe_path)

    def _handle_cookie_file_selection(self) -> None:
        """Handle cookie file selection dialog."""
        cookie_file, _ = QFileDialog.getOpenFileName(
            self, "Select Cookie File", "", "Text Files (*.txt);;All Files (*)"
        )

        if cookie_file:
            self._validate_and_set_cookie_file(cookie_file)

    def _guide_extension_installation(self, exe_path: Optional[str]) -> None:
        """Guide user through extension installation process."""
        # Chrome Web Store URL for the cookie extension
        ext_url = (
            "https://chromewebstore.google.com/detail/"
            "get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc"
        )

        # Open extension page in user's browser
        if exe_path and os.path.exists(exe_path):
            webbrowser.BackgroundBrowser(exe_path).open(ext_url)
        else:
            webbrowser.open(ext_url)

        # Prompt user to install and then select cookie file
        QMessageBox.information(
            self, "Cookie Extension",
            "Please install the extension, then select the cookie file."
        )

        # Let user select cookie file after installation
        self._handle_cookie_file_selection()

    def _validate_and_set_cookie_file(self, cookie_file: str) -> None:
        """
        Validate and set the cookie file for authentication.

        Args:
            cookie_file: Path to the cookie file
        """
        try:
            # Read and validate cookie file content
            with open(cookie_file, "r", encoding="utf-8", errors="ignore") as f:
                data = f.read()

            # Check if file contains YouTube cookies
            if "youtube.com" in data.lower():
                self.cookie_file = cookie_file
                self.use_cookies = True
                self.log_message(f"Cookie file set: {cookie_file}")
            else:
                QMessageBox.warning(
                    self, "Invalid Cookie File",
                    "The selected file doesn't appear to contain YouTube cookies."
                )
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Cannot read cookie file: {e}")

    def _open_youtube_login(self, exe_path: Optional[str]) -> None:
        """
        Open YouTube login page for user verification.

        Args:
            exe_path: Path to browser executable
        """
        login_url = "https://accounts.google.com/ServiceLogin?service=youtube"

        # Open login page in user's preferred browser
        if exe_path and os.path.exists(exe_path):
            webbrowser.BackgroundBrowser(exe_path).open(login_url)
        else:
            webbrowser.open(login_url)

        QMessageBox.information(
            self, "Login",
            "Please log in to YouTube in the browser, then click OK."
        )

    def show_about(self) -> None:
        """Display application about dialog."""
        about_text = (
            "SSTube Video Downloader\n"
            "Version 2.2.0\n\n"
            "Developed by Ujjwal Nova\n\n"
            "A professional YouTube video and audio downloader\n"
            "with support for playlists and channels.\n\n"
            "Report bugs via our support channel."
        )

        QMessageBox.information(self, "About SSTube", about_text)

    def update_status(self, message: str) -> None:
        """
        Update status bar message (thread-safe).

        Args:
            message: Status message to display
        """
        self.updateStatusSignal.emit(message)

    def _update_status(self, message: str) -> None:
        """Internal method to update status bar in main thread."""
        self.status_bar.showMessage(message)

    def log_message(self, msg: str) -> None:
        """
        Log message to activity panel and console (thread-safe).

        Args:
            msg: Message to log
        """
        self.logMessageSignal.emit(msg)
        print(f"[SSTube] {msg}")  # Also log to console

    def _log_message(self, msg: str) -> None:
        """Internal method to add message to log widget in main thread."""
        if hasattr(self, "log_text"):
            # Add timestamp for better logging
            from datetime import datetime
            timestamp = datetime.now().strftime("%H:%M:%S")
            formatted_msg = f"[{timestamp}] {msg}"
            self.log_text.append(formatted_msg)

    def create_sidebar(self) -> QWidget:
        """
        Create navigation sidebar with application pages.

        Returns:
            Widget containing sidebar navigation buttons
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Application title header
        header = QLabel("SSTube")
        header.setStyleSheet("font-size: 16pt; font-weight: bold;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        layout.addSpacing(20)

        # Navigation buttons
        nav_buttons = [
            ("Download", "download"),
            ("Activity", "activity")
        ]

        for name, icon_key in nav_buttons:
            btn = QPushButton(name)

            # Set icon if available
            icon = self.icons.get(icon_key)
            if icon:
                btn.setIcon(icon)
                btn.setIconSize(QSize(32, 32))

            # Connect to page switching
            btn.clicked.connect(lambda checked, n=name: self.switch_page(n))
            layout.addWidget(btn)

        # Push buttons to top
        layout.addStretch()

        return widget

    def switch_page(self, name: str) -> None:
        """
        Switch to the specified page in the main content area.

        Args:
            name: Name of the page to switch to ("Download" or "Activity")
        """
        if name == "Download":
            self.stack.setCurrentWidget(self.download_page)
        elif name == "Activity":
            self.stack.setCurrentWidget(self.activity_page)

        self.update_status(f"{name} section active")

    def create_download_page(self) -> QWidget:
        """
        Create the main download configuration page.

        Returns:
            Widget containing download configuration controls
        """
        page = QWidget()
        layout = QVBoxLayout(page)

        # URL input section
        layout.addWidget(QLabel(
            "Enter YouTube URL (or Playlist/Channel URL):",
            styleSheet="font-size: 12pt; font-weight: bold;"
        ))

        self.url_entry = QLineEdit()
        self.url_entry.setPlaceholderText("https://www.youtube.com/watch?v=...")
        layout.addWidget(self.url_entry)

        # Save location section
        layout.addWidget(QLabel(
            "Save Location:",
            styleSheet="font-size: 12pt; font-weight: bold;"
        ))

        path_layout = QHBoxLayout()
        self.path_entry = QLineEdit(readOnly=True)
        self.path_entry.setPlaceholderText("Select folder to save downloads")
        path_layout.addWidget(self.path_entry)

        browse_btn = QPushButton("Browse Folder")
        browse_btn.clicked.connect(self.select_save_path)
        path_layout.addWidget(browse_btn)
        layout.addLayout(path_layout)

        # Download mode section
        layout.addWidget(QLabel(
            "Download Mode:",
            styleSheet="font-size: 12pt; font-weight: bold;"
        ))

        self.mode_combo = QComboBox()
        download_modes = [
            "Single Video",  # Download single video
            "MP3 Only",  # Extract audio only
            "Playlist Video",  # Download playlist videos
            "Playlist MP3",  # Extract audio from playlist
            "Channel Videos",  # Download channel videos
            "Channel Videos MP3",  # Extract audio from channel videos
            "Channel Shorts",  # Download channel shorts
            "Channel Shorts MP3",  # Extract audio from channel shorts
        ]
        self.mode_combo.addItems(download_modes)
        self.mode_combo.currentTextChanged.connect(self.mode_changed)
        layout.addWidget(self.mode_combo)

        # Video quality section (hidden for audio-only modes)
        self.video_quality_label = QLabel(
            "Video Quality:",
            styleSheet="font-size: 12pt; font-weight: bold;"
        )
        self.video_quality_combo = QComboBox()
        quality_options = [
            "Best Available",  # Highest quality available
            "4320p 8K",  # 8K resolution
            "2160p 4K",  # 4K resolution
            "1440p 2K",  # 2K resolution
            "1080p Full HD",  # Full HD
            "720p HD",  # HD
            "480p Standard",  # Standard definition
            "360p Medium"  # Low quality
        ]
        self.video_quality_combo.addItems(quality_options)

        layout.addWidget(self.video_quality_label)
        layout.addWidget(self.video_quality_combo)

        # Initialize visibility based on default mode
        self.mode_changed(self.mode_combo.currentText())

        # Download button
        download_btn = QPushButton("Download")
        download_btn.setStyleSheet("font-size: 12pt; font-weight: bold; padding: 8px;")
        download_btn.clicked.connect(self.add_to_queue)
        layout.addWidget(download_btn)

        # Push content to top
        layout.addStretch()

        return page

    def mode_changed(self, text: str) -> None:
        """
        Handle download mode change to show/hide relevant controls.

        Args:
            text: Selected download mode text
        """
        self.mode_var = text

        # Hide video quality controls for audio-only modes
        if "MP3" in text:
            self.video_quality_label.hide()
            self.video_quality_combo.hide()
        else:
            self.video_quality_label.show()
            self.video_quality_combo.show()

    def select_save_path(self) -> None:
        """Open folder selection dialog for download location."""
        directory = QFileDialog.getExistingDirectory(
            self, "Select Download Folder"
        )

        if directory:
            self.path_entry.setText(directory)
            self.update_status("Save path selected")

    def add_to_queue(self) -> None:
        """
        Validate input and add download task to queue.

        This method handles different download modes and validates URLs
        before adding tasks to the download queue.
        """
        # Get and validate input
        url = self.url_entry.text().strip()
        save_path = self.path_entry.text().strip()
        mode = self.mode_combo.currentText()

        if not url or not save_path:
            QMessageBox.critical(
                self, "Error",
                "Please enter a URL and select a save path."
            )
            return

        # Handle different download modes
        if mode in ["Playlist Video", "Playlist MP3"]:
            self._handle_playlist_download(url, save_path, mode)
        elif mode in ["Channel Videos", "Channel Videos MP3", "Channel Shorts", "Channel Shorts MP3"]:
            self._handle_channel_download(url, save_path, mode)
        else:
            # Single video or MP3 only
            self._handle_single_download(url, save_path, mode)

    def _handle_playlist_download(self, url: str, save_path: str, mode: str) -> None:
        """Handle playlist download mode."""
        # Validate playlist URL
        if "list=" not in url:
            QMessageBox.critical(
                self, "Error",
                "The URL does not appear to be a playlist URL.\n"
                "Playlist URLs should contain 'list=' parameter."
            )
            return

        self.process_playlist(url, save_path, mode)

    def _handle_channel_download(self, url: str, save_path: str, mode: str) -> None:
        """Handle channel download mode."""
        # Validate channel URL
        if "youtube.com/@" not in url and "/channel/" not in url:
            QMessageBox.critical(
                self, "Error",
                "The URL does not appear to be a channel URL.\n"
                "Channel URLs should contain '@' or '/channel/'."
            )
            return

        # Check for query parameters that might cause issues
        if "?" in url:
            QMessageBox.critical(
                self, "Error",
                "Please use a clean channel URL without query parameters.\n"
                "Example: https://www.youtube.com/@channelname"
            )
            return

        self.process_channel(url, save_path, mode)

    def _handle_single_download(self, url: str, save_path: str, mode: str) -> None:
        """Handle single video or MP3-only download."""
        # Create download task
        task = {
            "url": url,
            "save_path": save_path,
            "mode": mode,
            "audio_quality": self.audio_quality_default if "MP3" in mode else None,
            "video_quality": self.video_quality_combo.currentText() if "MP3" not in mode else "Best Available",
        }

        self.download_queue.append(task)
        self.log_message(f"Task added to queue: {mode}")
        self.process_queue()

    def process_playlist(self, url: str, save_path: str, mode: str) -> None:
        """
        Process playlist URL and show video selection dialog.

        Args:
            url: Playlist URL
            save_path: Download destination path
            mode: Download mode (Playlist Video/MP3)
        """
        try:
            # Use yt-dlp.exe to extract playlist information
            yt_dlp_path = os.path.join(self.base_dir, "bin", "yt-dlp.exe")
            cmd = [yt_dlp_path, "--quiet", "--flat-playlist", "--dump-json", url]

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            entries = []
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    try:
                        entry = json.loads(line)
                        entries.append(entry)
                    except json.JSONDecodeError:
                        continue

            if not entries:
                QMessageBox.warning(
                    self, "Warning",
                    "No videos found in the playlist."
                )
                return

        except Exception as e:
            QMessageBox.critical(
                self, "Error",
                f"Failed to extract playlist information: {e}"
            )
            return

        # Show video selection dialog
        self._show_video_selection_dialog(
            entries, save_path, mode, "Select Videos from Playlist"
        )

    def process_channel(self, url: str, save_path: str, mode: str) -> None:
        """
        Process channel URL and show video selection dialog.

        Args:
            url: Channel URL
            save_path: Download destination path
            mode: Download mode (Channel Videos/MP3 or Channel Shorts/MP3)
        """
        # Append appropriate suffix based on content type
        suffix = "/videos" if "Videos" in mode else "/shorts"
        if not url.lower().endswith(suffix):
            url = url.rstrip("/") + suffix

        try:
            # Use yt-dlp.exe to extract channel information
            yt_dlp_path = os.path.join(self.base_dir, "bin", "yt-dlp.exe")
            cmd = [yt_dlp_path, "--quiet", "--flat-playlist", "--dump-json", url]

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            entries = []
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    try:
                        entry = json.loads(line)
                        entries.append(entry)
                    except json.JSONDecodeError:
                        continue

            # Filter entries based on content type
            if "Shorts" in mode:
                # Filter for shorts content
                entries = [e for e in entries if "shorts" in e.get("url", "").lower()]
            else:
                # Filter out shorts for regular videos
                entries = [e for e in entries if "shorts" not in e.get("url", "").lower()]

            if not entries:
                content_type = "shorts" if "Shorts" in mode else "videos"
                QMessageBox.warning(
                    self, "Warning",
                    f"No {content_type} found in the channel."
                )
                return

        except Exception as e:
            QMessageBox.critical(
                self, "Error",
                f"Failed to extract channel information: {e}"
            )
            return

        # Show video selection dialog
        dialog_title = "Select Videos from Channel" if "Videos" in mode else "Select Shorts from Channel"
        self._show_video_selection_dialog(entries, save_path, mode, dialog_title)

    def _show_video_selection_dialog(self, entries: List[Dict], save_path: str, mode: str, title: str) -> None:
        """
        Show dialog for selecting videos from playlist or channel.

        Args:
            entries: List of video entries
            save_path: Download destination path
            mode: Download mode
            title: Dialog window title
        """
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.resize(600, 400)

        # Main layout
        dlg_layout = QVBoxLayout(dialog)

        # Info label
        info_label = QLabel(f"Found {len(entries)} videos. Select videos to download:")
        info_label.setStyleSheet("font-weight: bold; margin-bottom: 10px;")
        dlg_layout.addWidget(info_label)

        # Scrollable area for video list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        dlg_layout.addWidget(scroll)

        container = QWidget()
        scroll.setWidget(container)
        scroll_layout = QVBoxLayout(container)

        # Create checkboxes for each video
        checkboxes = []
        for entry in entries:
            video_url = entry.get("url")

            # Ensure URL is absolute
            if video_url and not video_url.startswith("http"):
                base_url = entry.get("webpage_url", "https://www.youtube.com")
                video_url = base_url.rstrip("/") + "/" + video_url.lstrip("/")

            # Create checkbox with video title
            title = entry.get("title", "Unknown Title")
            cb = QCheckBox(title)

            # Add video favicon if available
            if self.video_favicon_pixmap:
                cb.setIcon(QIcon(self.video_favicon_pixmap))

            # Default to checked
            cb.setChecked(True)

            scroll_layout.addWidget(cb)
            checkboxes.append((video_url, cb))

        # Button layout
        button_layout = QHBoxLayout()

        # Select All / Deselect All buttons
        select_all_btn = QPushButton("Select All")
        select_all_btn.clicked.connect(
            lambda: [cb.setChecked(True) for _, cb in checkboxes]
        )
        button_layout.addWidget(select_all_btn)

        deselect_all_btn = QPushButton("Deselect All")
        deselect_all_btn.clicked.connect(
            lambda: [cb.setChecked(False) for _, cb in checkboxes]
        )
        button_layout.addWidget(deselect_all_btn)

        button_layout.addStretch()

        # Cancel button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_btn)

        # Download Selected button
        download_btn = QPushButton("Download Selected")
        download_btn.setStyleSheet("font-weight: bold;")
        download_btn.clicked.connect(
            lambda: self._process_selected_videos(checkboxes, save_path, mode, dialog)
        )
        button_layout.addWidget(download_btn)

        dlg_layout.addLayout(button_layout)

        # Show dialog
        dialog.exec()

    def _process_selected_videos(self, checkboxes: List[Tuple], save_path: str, mode: str, dialog: QDialog) -> None:
        """
        Process selected videos and add them to download queue.

        Args:
            checkboxes: List of (video_url, checkbox) tuples
            save_path: Download destination path
            mode: Download mode
            dialog: Parent dialog to close
        """
        selected_count = 0

        # Add selected videos to download queue
        for video_url, cb in checkboxes:
            if cb.isChecked() and video_url:
                task = {
                    "url": video_url,
                    "save_path": save_path,
                    "mode": mode,
                    "audio_quality": self.audio_quality_default if "MP3" in mode else None,
                    "video_quality": self.video_quality_combo.currentText() if "MP3" not in mode else "Best Available",
                }
                self.download_queue.append(task)
                selected_count += 1

        if selected_count == 0:
            QMessageBox.warning(dialog, "Warning", "No videos selected for download.")
            return

        # Log and start processing
        self.log_message(f"Added {selected_count} videos to download queue")
        dialog.accept()

        # Switch to activity page and start downloads
        self.switch_page("Activity")
        self.process_queue()

    def create_activity_page(self) -> QWidget:
        """
        Create the activity/logging page for monitoring downloads.

        Returns:
            Widget containing activity log and progress information
        """
        page = QWidget()
        layout = QVBoxLayout(page)

        # Page title
        title_label = QLabel("Download Activity")
        title_label.setStyleSheet("font-size: 14pt; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title_label)

        # Log text area
        self.log_text = QTextEdit(readOnly=True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 9pt;
                background-color: black;
                color: white;
                border: 1px solid #ccc;
            }
        """)
        layout.addWidget(self.log_text)

        # Control buttons
        button_layout = QHBoxLayout()

        # Clear log button
        clear_btn = QPushButton("Clear Log")
        clear_btn.clicked.connect(lambda: self.log_text.clear())
        button_layout.addWidget(clear_btn)

        button_layout.addStretch()

        # Queue status label
        self.queue_status_label = QLabel("Queue: 0 pending")
        self.queue_status_label.setStyleSheet("font-weight: bold;")
        button_layout.addWidget(self.queue_status_label)

        layout.addLayout(button_layout)

        return page

    def process_queue(self) -> None:
        """
        Process the download queue by starting the next download.

        This method ensures only one download runs at a time and automatically
        processes the next item in the queue when the current download completes.
        """
        # Update queue status
        if hasattr(self, 'queue_status_label'):
            self.queue_status_label.setText(f"Queue: {len(self.download_queue)} pending")

        # Start next download if not already downloading and queue has items
        if not self.downloading and self.download_queue:
            task = self.download_queue.pop(0)
            self.downloading = True

            # Start download in background thread
            threading.Thread(
                target=self.download_video,
                args=(task,),
                daemon=True
            ).start()

    def download_video(self, task: Dict[str, Any]) -> None:
        """
        Download video/audio based on task configuration using yt-dlp.exe.

        Args:
            task: Dictionary containing download configuration
                - url: Video URL
                - save_path: Download destination
                - mode: Download mode
                - audio_quality: Audio quality for MP3 extraction
                - video_quality: Video quality preference

        This method runs in a background thread to avoid blocking the UI.
        """
        url = task["url"]
        save_path = task["save_path"]
        mode = task["mode"]
        video_quality = task.get("video_quality", "Best Available")

        self.update_status(f"Starting download: {os.path.basename(url)}")

        try:
            # Get yt-dlp.exe path
            yt_dlp_path = os.path.join(self.base_dir, "bin", "yt-dlp.exe")
            ffmpeg_path = os.path.join(self.base_dir, "bin", "ffmpeg.exe")

            # Build command based on mode
            if "Video" in mode and "MP3" not in mode:
                # Video download
                cmd = self._build_video_download_command(yt_dlp_path, ffmpeg_path, url, save_path, video_quality)
            else:
                # Audio extraction
                cmd = self._build_audio_download_command(yt_dlp_path, ffmpeg_path, url, save_path,
                                                         task.get("audio_quality", "320"))

            # Add cookie support if enabled
            if self.use_cookies and self.cookie_file:
                cmd.extend(["--cookies", self.cookie_file])
                self.log_message("Using cookie file for authentication")

            # Get video info first for logging
            info_cmd = [yt_dlp_path, "--quiet", "--dump-json", "--no-playlist", url]
            if self.use_cookies and self.cookie_file:
                info_cmd.extend(["--cookies", self.cookie_file])

            try:
                info_result = subprocess.run(info_cmd, capture_output=True, text=True, check=True)
                info = json.loads(info_result.stdout)
                title = info.get("title", "Unknown Title")
            except:
                title = "Unknown Title"

            self.log_message(f"Starting download: {title}")

            # Execute download command
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                       text=True, universal_newlines=True)

            # Read output line by line for progress updates
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    line = output.strip()
                    if line:
                        self.log_message(line)

            # Check if download was successful
            if process.returncode == 0:
                self.log_message(f"Download completed: {title}")
            else:
                raise subprocess.CalledProcessError(process.returncode, cmd)

        except Exception as e:
            error_msg = f"Download failed for {url}: {str(e)}"
            self.log_message(error_msg)

            # Show detailed error dialog in main thread
            QTimer.singleShot(0, lambda: self._show_download_error(e))

        finally:
            # Mark download as complete and process next in queue
            self.downloading = False
            QTimer.singleShot(100, self.process_queue)  # Small delay to update UI

    def _build_video_download_command(self, yt_dlp_path: str, ffmpeg_path: str, url: str, save_path: str,
                                      video_quality: str) -> List[str]:
        """
        Build yt-dlp.exe command for video download.

        Args:
            yt_dlp_path: Path to yt-dlp.exe
            ffmpeg_path: Path to ffmpeg.exe
            url: Video URL
            save_path: Download destination path
            video_quality: Preferred video quality

        Returns:
            List of command arguments
        """
        cmd = [
            yt_dlp_path,
            "--ffmpeg-location", ffmpeg_path,
            "--no-playlist",
            "--output", os.path.join(save_path, "%(title)s.%(ext)s"),
            "--format", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
            "--merge-output-format", "mp4",
            url
        ]

        # Apply quality filter if not "Best Available"
        if video_quality != "Best Available":
            height = video_quality.split("p")[0]
            cmd[cmd.index("--format") + 1] = f"bestvideo[height<={height}]+bestaudio/merge"

        return cmd

    def _build_audio_download_command(self, yt_dlp_path: str, ffmpeg_path: str, url: str, save_path: str,
                                      audio_quality: str) -> List[str]:
        """
        Build yt-dlp.exe command for audio extraction.

        Args:
            yt_dlp_path: Path to yt-dlp.exe
            ffmpeg_path: Path to ffmpeg.exe
            url: Video URL
            save_path: Download destination path
            audio_quality: Audio quality in kbps

        Returns:
            List of command arguments
        """
        cmd = [
            yt_dlp_path,
            "--ffmpeg-location", ffmpeg_path,
            "--no-playlist",
            "--output", os.path.join(save_path, "%(title)s.%(ext)s"),
            "--format", "bestaudio/best",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", audio_quality,
            url
        ]

        return cmd

    def _show_download_error(self, error: Exception) -> None:
        """
        Show detailed download error dialog.

        Args:
            error: Exception that occurred during download
        """
        error_text = str(error)

        # Add helpful hints for common errors
        if "Failed to decrypt with DPAPI" in error_text:
            error_text += (
                "\n\nTroubleshooting tips:\n"
                "• Ensure Chrome is completely closed\n"
                "• Run SSTube as the same user who uses Chrome\n"
                "• Try exporting cookies manually\n"
                "• Check if cookie file is recent and valid"
            )
        elif "HTTP Error 403" in error_text:
            error_text += (
                "\n\nThis might be a private or age-restricted video.\n"
                "Try logging in with cookies or check if the video is accessible."
            )
        elif "Video unavailable" in error_text:
            error_text += (
                "\n\nThe video might be:\n"
                "• Deleted or made private\n"
                "• Geo-blocked in your region\n"
                "• Age-restricted (try using cookies)"
            )

        QMessageBox.critical(
            self, "Download Error",
            f"Download failed:\n\n{error_text}"
        )


def main():
    """
    Main application entry point.

    Initializes the Qt application and starts the main event loop.
    """
    # Create Qt application
    app = QApplication(sys.argv)

    # Set application metadata
    app.setApplicationName("SSTube")
    app.setApplicationVersion("2.2.0")
    app.setOrganizationName("Ujjwal Nova")

    # Create and show main window
    window = SSTubeGUI()
    window.show()

    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()