"""
Handles creation and management of the UI.
"""

import os
from typing import TYPE_CHECKING

from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QStackedWidget,
    QStatusBar,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtGui import QAction, QIcon, QPixmap
from PyQt6.QtCore import QSize, Qt

if TYPE_CHECKING:
    from .main_window import YTDGUI


class UIManager:
    """Handles creation and management of the UI."""

    def __init__(self, main_app: "YTDGUI"):
        self.main_app = main_app
        self.main_app.icons = {}
        self.main_app.video_favicon_pixmap = None

    def _load_stylesheet(self) -> None:
        """Load and apply the application stylesheet."""
        try:
            style_path = os.path.join(self.main_app.base_dir, "assets", "style.qss")
            if os.path.exists(style_path):
                with open(style_path, "r") as f:
                    self.main_app.setStyleSheet(f.read())
        except Exception as e:
            print(f"Error loading stylesheet: {e}")

    def _set_window_icon(self) -> None:
        """Set the application window icon if available."""
        try:
            icon_path = os.path.join(self.main_app.base_dir, "favicon.ico")
            if os.path.exists(icon_path):
                self.main_app.setWindowIcon(QIcon(icon_path))
        except Exception:
            # Silently continue if icon cannot be loaded
            pass

    def _load_icons(self) -> None:
        """Load application icons from assets directory."""
        self.main_app.icons = {
            "download": self.load_icon(
                os.path.join(self.main_app.base_dir, "assets", "download.png")
            ),
            "activity": self.load_icon(
                os.path.join(self.main_app.base_dir, "assets", "activity.png")
            ),
        }

        # Load video favicon for playlist/channel selection dialogs
        try:
            vf_path = os.path.join(
                self.main_app.base_dir, "assets", "video-favicon.png"
            )
            if os.path.exists(vf_path):
                self.main_app.video_favicon_pixmap = QPixmap(vf_path).scaled(
                    16,
                    16,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            else:
                self.main_app.video_favicon_pixmap = None
        except Exception:
            self.main_app.video_favicon_pixmap = None

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
        menubar = self.main_app.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        # Login action for cookie-based authentication
        login_action = QAction("Login", self.main_app)
        login_action.triggered.connect(self.main_app.login_manager.open_login)
        file_menu.addAction(login_action)

        file_menu.addSeparator()

        # Exit action
        exit_action = QAction("Exit", self.main_app)
        exit_action.triggered.connect(self.main_app.close)
        file_menu.addAction(exit_action)

        # Help menu
        help_menu = menubar.addMenu("Help")

        # About dialog
        about_action = QAction("About", self.main_app)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def show_about(self) -> None:
        """Display application about dialog."""
        about_text = (
            "yt-downloader-gui\n"
            "Version 2.4.0\n\n"
            "Developed by Ujjwal Nova\n\n"
            "A professional YouTube video and audio downloader\n"
            "with support for playlists and channels.\n\n"
            "Report bugs via our support channel."
        )

        QMessageBox.information(self.main_app, "About yt-downloader-gui", about_text)

    def create_sidebar(self) -> QWidget:
        """
        Create navigation sidebar with application pages.

        Returns:
            Widget containing sidebar navigation buttons
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Application title header
        header = QLabel("yt-downloader-gui")
        header.setObjectName("header")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        layout.addSpacing(20)

        # Navigation buttons
        nav_buttons = [("Download", "download"), ("Activity", "activity")]

        for name, icon_key in nav_buttons:
            btn = QPushButton(name)

            # Set icon if available
            icon = self.main_app.icons.get(icon_key)
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
            self.main_app.stack.setCurrentWidget(self.main_app.download_page)
        elif name == "Activity":
            self.main_app.stack.setCurrentWidget(self.main_app.activity_page)

        self.main_app.update_status(f"{name} section active")

    def create_download_page(self) -> QWidget:
        """
        Create the main download configuration page.

        Returns:
            Widget containing download configuration controls
        """
        page = QWidget()
        layout = QVBoxLayout(page)

        # URL input section
        url_label = QLabel("Enter YouTube URL (or Playlist/Channel URL):")
        url_label.setObjectName("header_label")
        layout.addWidget(url_label)

        self.main_app.url_entry = QLineEdit()
        self.main_app.url_entry.setPlaceholderText(
            "https://www.youtube.com/watch?v=..."
        )
        layout.addWidget(self.main_app.url_entry)

        # Save location section
        save_path_label = QLabel("Save Location:")
        save_path_label.setObjectName("header_label")
        layout.addWidget(save_path_label)

        path_layout = QHBoxLayout()
        self.main_app.path_entry = QLineEdit(readOnly=True)
        self.main_app.path_entry.setPlaceholderText("Select folder to save downloads")
        path_layout.addWidget(self.main_app.path_entry)

        browse_btn = QPushButton("Browse Folder")
        browse_btn.clicked.connect(self.main_app.select_save_path)
        path_layout.addWidget(browse_btn)
        layout.addLayout(path_layout)

        # Download mode section
        mode_label = QLabel("Download Mode:")
        mode_label.setObjectName("header_label")
        layout.addWidget(mode_label)

        self.main_app.mode_combo = QComboBox()
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
        self.main_app.mode_combo.addItems(download_modes)
        self.main_app.mode_combo.currentTextChanged.connect(self.mode_changed)
        layout.addWidget(self.main_app.mode_combo)

        # Video quality section (hidden for audio-only modes)
        self.main_app.video_quality_label = QLabel("Video Quality:")
        self.main_app.video_quality_label.setObjectName("header_label")
        self.main_app.video_quality_combo = QComboBox()
        quality_options = [
            "Best Available",  # Highest quality available
            "4320p 8K",  # 8K resolution
            "2160p 4K",  # 4K resolution
            "1440p 2K",  # 2K resolution
            "1080p Full HD",  # Full HD
            "720p HD",  # HD
            "480p Standard",  # Standard definition
            "360p Medium",  # Low quality
        ]
        self.main_app.video_quality_combo.addItems(quality_options)

        layout.addWidget(self.main_app.video_quality_label)
        layout.addWidget(self.main_app.video_quality_combo)

        # Initialize visibility based on default mode
        self.mode_changed(self.main_app.mode_combo.currentText())

        # Download button
        download_btn = QPushButton("Download")
        download_btn.setObjectName("download_button")
        download_btn.clicked.connect(self.main_app.download_manager.add_to_queue)
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
        self.main_app.mode_var = text

        # Hide video quality controls for audio-only modes
        if "MP3" in text:
            self.main_app.video_quality_label.hide()
            self.main_app.video_quality_combo.hide()
        else:
            self.main_app.video_quality_label.show()
            self.main_app.video_quality_combo.show()

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
        title_label.setObjectName("header_label")
        layout.addWidget(title_label)

        # Progress bar
        self.main_app.progress_bar = QProgressBar()
        self.main_app.progress_bar.setObjectName("progress_bar")
        self.main_app.progress_bar.setTextVisible(True)
        self.main_app.progress_bar.setValue(0)
        layout.addWidget(self.main_app.progress_bar)

        # Log text area
        self.main_app.log_text = QTextEdit(readOnly=True)
        layout.addWidget(self.main_app.log_text)

        # Control buttons
        button_layout = QHBoxLayout()

        # Clear log button
        clear_btn = QPushButton("Clear Log")
        clear_btn.clicked.connect(lambda: self.main_app.log_text.clear())
        button_layout.addWidget(clear_btn)

        button_layout.addStretch()

        # Queue status label
        self.main_app.queue_status_label = QLabel("Queue: 0 pending")
        self.main_app.queue_status_label.setObjectName("status_label")
        button_layout.addWidget(self.main_app.queue_status_label)

        layout.addLayout(button_layout)

        return page

    def _create_ui(self) -> None:
        """Create and layout the main user interface."""
        # Load stylesheet
        self._load_stylesheet()

        # Create menu bar
        self.create_menubar()

        # Central widget with horizontal layout
        central_widget = QWidget()
        self.main_app.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        # Sidebar navigation
        self.main_app.sidebar = self.create_sidebar()
        layout.addWidget(self.main_app.sidebar)

        # Main content area with stacked pages
        self.main_app.stack = QStackedWidget()
        self.main_app.download_page = self.create_download_page()
        self.main_app.activity_page = self.create_activity_page()
        self.main_app.stack.addWidget(self.main_app.download_page)
        self.main_app.stack.addWidget(self.main_app.activity_page)
        layout.addWidget(self.main_app.stack, 1)  # Expand to fill available space

        # Status bar
        self.main_app.status_bar = QStatusBar()
        self.main_app.setStatusBar(self.main_app.status_bar)
