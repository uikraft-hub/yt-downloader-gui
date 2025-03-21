import os
import sys
import threading
import webbrowser
import yt_dlp

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

# Define current version of SSTube (for reference)
CURRENT_VERSION = "2.0"


class SSTubeGUI(QMainWindow):
    updateStatusSignal = pyqtSignal(str)
    logMessageSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SSTube")
        self.resize(400, 300)

        # Determine base directory (works for both script and frozen exe)
        if getattr(sys, "frozen", False):
            self.base_dir = os.path.dirname(sys.executable)
        else:
            self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # Set window icon from Favicon.png
        try:
            icon_path = os.path.join(self.base_dir, "Favicon.png")
            self.setWindowIcon(QIcon(icon_path))
        except Exception as e:
            print("Error setting window icon:", e)

        # Download queue (history functions have been removed)
        self.download_queue = []
        self.download_thread = None
        self.downloading = False  # Flag for sequential downloads

        # Mode selection variable and quality defaults
        self.mode_var = "Single Video"
        # For MP3 modes we now always download best available (hardcoded as "320")
        self.audio_quality_default = "320"
        self.video_quality = "Best Available"  # For video modes

        # Use cookies from browser if user logs in
        self.use_cookies = False
        # Default browser for cookie extraction (will be set by the user)
        self.cookie_browser = "chrome"

        # Load sidebar icons from assets folder (settings icon removed)
        self.icons = {
            "download": self.load_icon(
                os.path.join(self.base_dir, "assets", "download.png")
            ),
            "activity": self.load_icon(
                os.path.join(self.base_dir, "assets", "activity.png")
            ),
        }

        # Load video favicon for selection dialogs
        try:
            vf_path = os.path.join(self.base_dir, "assets", "video-favicon.png")
            self.video_favicon = QIcon(vf_path)
            self.video_favicon_pixmap = QPixmap(vf_path).scaled(
                16,
                16,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        except Exception as e:
            print("Error loading video favicon:", e)
            self.video_favicon = None
            self.video_favicon_pixmap = None

        # Create menubar
        self.create_menubar()

        # Central widget with a horizontal layout: sidebar + stacked pages
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Create sidebar
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar)

        # Create a QStackedWidget to hold the pages
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget, 1)

        # Create pages: Download and Activity (Settings removed)
        self.download_page = self.create_download_page()
        self.activity_page = self.create_activity_page()

        self.stacked_widget.addWidget(self.download_page)
        self.stacked_widget.addWidget(self.activity_page)

        # Setup status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.update_status("Ready")

        # Connect signals for thread-safe UI updates
        self.updateStatusSignal.connect(self._update_status)
        self.logMessageSignal.connect(self._log_message)

    def load_icon(self, path):
        try:
            pixmap = QPixmap(path)
            return QIcon(pixmap)
        except Exception as e:
            print(f"Error loading icon {path}: {e}")
            return QIcon()

    def create_menubar(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        # New Login action added
        login_action = QAction("Login", self)
        login_action.triggered.connect(self.open_login)
        file_menu.addAction(login_action)
        help_menu = menubar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def get_installed_browsers(self):
        browsers = []
        try:
            import winreg

            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Clients\StartMenuInternet"
            )
            i = 0
            while True:
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    browsers.append(subkey_name)
                    i += 1
                except OSError:
                    break
        except Exception:
            pass
        if not browsers:
            # Fallback default list
            browsers = ["Google Chrome", "Mozilla Firefox", "Microsoft Edge"]
        return browsers

    def map_browser(self, browser_name):
        name = browser_name.lower()
        if "chrome" in name:
            return "chrome"
        elif "firefox" in name:
            return "firefox"
        elif "edge" in name:
            return "edge"
        elif "opera" in name:
            return "opera"
        else:
            return browser_name.lower()

    def open_login(self):
        if self.use_cookies:
            QMessageBox.information(
                self,
                "Login",
                "You are already logged in. Your browser's cookies are being used.",
            )
        else:
            installed = self.get_installed_browsers()
            # Show the list of installed browsers to the user
            browser_choice, ok = QInputDialog.getItem(
                self,
                "Select Browser",
                "Select the browser you use for YouTube login:",
                installed,
                0,
                False,
            )
            if ok and browser_choice:
                self.cookie_browser = self.map_browser(browser_choice)
            else:
                self.cookie_browser = "chrome"
            login_url = "https://accounts.google.com/ServiceLogin?service=youtube"
            # Dictionary mapping browser identifiers to common executable paths
            browser_paths = {
                "chrome": r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
                "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                "opera": r"C:\Program Files\Opera\launcher.exe",
                "brave": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
            }
            exe_path = browser_paths.get(self.cookie_browser, None)
            if exe_path and os.path.exists(exe_path):
                controller = webbrowser.BackgroundBrowser(exe_path)
                controller.open(login_url)
            else:
                # Fallback to default if path not found
                webbrowser.open(login_url)
            # Ask user to confirm after successful login
            QMessageBox.information(
                self,
                "Login",
                f"Your selected browser ({self.cookie_browser}) has been opened.\n"
                "Please log in to your YouTube account.\n"
                "After logging in, click OK to continue.",
            )
            self.use_cookies = True
            QMessageBox.information(
                self, "Login", "Cookie is now being used for downloads."
            )

    def show_about(self):
        QMessageBox.information(
            self,
            "About SSTube",
            "SSTube Video Downloader\nVersion 2.0\nDeveloped by UKR\n\n"
            "Report bugs via our support channel.",
        )

    def update_status(self, message):
        self.updateStatusSignal.emit(message)

    def _update_status(self, message):
        self.status_bar.showMessage(message)

    def log_message(self, msg):
        self.logMessageSignal.emit(msg)
        print(msg)

    def _log_message(self, msg):
        if hasattr(self, "log_text"):
            self.log_text.append(msg)

    def create_sidebar(self):
        sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout()
        sidebar_widget.setLayout(sidebar_layout)
        header = QLabel("SSTube")
        header.setStyleSheet("font-size: 16pt; font-weight: bold;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(header)
        sidebar_layout.addSpacing(20)
        # Only two options: Download and Activity
        self.sidebar_buttons = {}
        for option in ["Download", "Activity"]:
            btn = QPushButton(option)
            if option.lower() in self.icons:
                btn.setIcon(self.icons[option.lower()])
            btn.setIconSize(QSize(32, 32))
            btn.clicked.connect(lambda checked, opt=option: self.show_page(opt))
            sidebar_layout.addWidget(btn)
            self.sidebar_buttons[option] = btn
        sidebar_layout.addStretch()
        return sidebar_widget

    def show_page(self, name):
        if name == "Download":
            self.stacked_widget.setCurrentWidget(self.download_page)
        elif name == "Activity":
            self.stacked_widget.setCurrentWidget(self.activity_page)
        self.update_status(f"{name} section active")

    def create_download_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        page.setLayout(layout)

        url_label = QLabel("Enter YouTube URL (or Playlist/Channel URL):")
        url_label.setStyleSheet("font-size: 12pt;")
        layout.addWidget(url_label)

        self.url_entry = QLineEdit()
        self.url_entry.setPlaceholderText("Enter URL here")
        layout.addWidget(self.url_entry)

        path_label = QLabel("Save Location:")
        path_label.setStyleSheet("font-size: 12pt;")
        layout.addWidget(path_label)

        path_layout = QHBoxLayout()
        self.path_entry = QLineEdit()
        self.path_entry.setReadOnly(True)
        path_layout.addWidget(self.path_entry)
        browse_btn = QPushButton("Browse Folder")
        browse_btn.clicked.connect(self.select_save_path)
        path_layout.addWidget(browse_btn)
        layout.addLayout(path_layout)

        mode_label = QLabel("Download Mode:")
        mode_label.setStyleSheet("font-size: 12pt;")
        layout.addWidget(mode_label)

        self.mode_combo = QComboBox()
        modes = [
            "Single Video",
            "MP3 Only",
            "Playlist Video",
            "Playlist MP3",
            "Channel Videos",
            "Channel Videos MP3",
            "Channel Shorts",
            "Channel Shorts MP3",
        ]
        self.mode_combo.addItems(modes)
        self.mode_combo.currentTextChanged.connect(self.mode_changed)
        layout.addWidget(self.mode_combo)

        # Quality selection widgets (only for video modes)
        self.video_quality_label = QLabel("Video Quality:")
        self.video_quality_combo = QComboBox()
        self.video_quality_combo.addItems(
            [
                "Best Available",
                "4320p 8K",
                "2160p 4K",
                "1440p 2K",
                "1080p Full HD",
                "720p HD",
                "480p Standard",
                "360p Medium",
            ]
        )
        layout.addWidget(self.video_quality_label)
        layout.addWidget(self.video_quality_combo)
        # When an MP3 mode is selected, hide video quality options.
        self.mode_changed(self.mode_combo.currentText())

        download_btn = QPushButton("Download")
        download_btn.clicked.connect(self.add_to_queue)
        layout.addWidget(download_btn)

        layout.addStretch()
        return page

    def mode_changed(self, text):
        self.mode_var = text
        if "MP3" in text:
            # For MP3 modes, do not show any quality selection
            self.video_quality_label.hide()
            self.video_quality_combo.hide()
        else:
            self.video_quality_label.show()
            self.video_quality_combo.show()

    def select_save_path(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Folder")
        if directory:
            self.path_entry.setText(directory)
            self.update_status("Save path selected")

    def add_to_queue(self):
        url = self.url_entry.text().strip()
        save_path = self.path_entry.text().strip()
        mode = self.mode_combo.currentText()
        if not url or not save_path:
            QMessageBox.critical(
                self, "Error", "Please enter a URL and select a save path."
            )
            return

        # Validate URL based on mode:
        if mode in ["Single Video", "MP3 Only"]:
            if "list=" in url or "youtube.com/@" in url or "/channel/" in url:
                QMessageBox.critical(
                    self,
                    "Error",
                    "The URL appears to be a playlist or channel. Please select the appropriate mode.",
                )
                return
        elif mode in ["Playlist Video", "Playlist MP3"]:
            if "list=" not in url:
                QMessageBox.critical(
                    self,
                    "Error",
                    "The URL does not appear to be a playlist. Please select the appropriate mode.",
                )
                return
        elif mode in [
            "Channel Videos",
            "Channel Videos MP3",
            "Channel Shorts",
            "Channel Shorts MP3",
        ]:
            if ("youtube.com/@" not in url) and ("/channel/" not in url):
                QMessageBox.critical(
                    self,
                    "Error",
                    "The URL does not appear to be a channel. Please select the appropriate mode.",
                )
                return
            if "?" in url:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Please use a clean channel URL (e.g. https://youtube.com/@username) without query parameters.",
                )
                return

        if mode in ["Playlist Video", "Playlist MP3"]:
            self.process_playlist(url, save_path, mode)
        elif mode in [
            "Channel Videos",
            "Channel Videos MP3",
            "Channel Shorts",
            "Channel Shorts MP3",
        ]:
            self.process_channel(url, save_path, mode)
        else:
            task = {
                "url": url,
                "save_path": save_path,
                "mode": mode,
                "audio_quality": self.audio_quality_default if "MP3" in mode else None,
                "video_quality": (
                    self.video_quality_combo.currentText()
                    if mode not in ["MP3 Only"]
                    else "Best Available"
                ),
            }
            self.download_queue.append(task)
            self.log_message("Task added to queue")
            self.process_queue()

    def process_playlist(self, url, save_path, mode):
        try:
            opts = {"quiet": True, "extract_flat": True}
            with yt_dlp.YoutubeDL(opts) as ydl:
                playlist_info = ydl.extract_info(url, download=False)
            if "entries" not in playlist_info:
                QMessageBox.critical(self, "Error", "No playlist entries found.")
                return
            entries = playlist_info["entries"]
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to extract playlist info: {e}")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Select Videos from Playlist")
        dialog.resize(600, 400)
        dlg_layout = QVBoxLayout()
        dialog.setLayout(dlg_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        dlg_layout.addWidget(scroll_area)
        container = QWidget()
        scroll_layout = QVBoxLayout()
        container.setLayout(scroll_layout)
        scroll_area.setWidget(container)

        self.playlist_checkboxes = []
        for entry in entries:
            if not entry:
                continue
            video_url = entry.get("url")
            if video_url and not video_url.startswith("http"):
                video_url = playlist_info.get("webpage_url", "") + video_url
            title = entry.get("title", "Unknown Title")
            checkbox = QCheckBox(title)
            if self.video_favicon_pixmap:
                checkbox.setIcon(QIcon(self.video_favicon_pixmap))
            checkbox.setChecked(True)
            scroll_layout.addWidget(checkbox)
            self.playlist_checkboxes.append((video_url, title, checkbox))

        download_btn = QPushButton("Download Selected")
        dlg_layout.addWidget(download_btn)

        def download_selected():
            count = 0
            for video_url, title, checkbox in self.playlist_checkboxes:
                if checkbox.isChecked():
                    task = {
                        "url": video_url,
                        "save_path": save_path,
                        "mode": mode,
                        "audio_quality": (
                            self.audio_quality_default if "MP3" in mode else None
                        ),
                        "video_quality": (
                            self.video_quality_combo.currentText()
                            if mode == "Playlist Video"
                            else "Best Available"
                        ),
                    }
                    self.download_queue.append(task)
                    count += 1
            if count == 0:
                QMessageBox.information(dialog, "Info", "No videos selected.")
            else:
                self.log_message(f"{count} videos added to queue from playlist.")
                self.process_queue()
            dialog.accept()

        download_btn.clicked.connect(download_selected)
        dialog.exec()

    def process_channel(self, url, save_path, mode):
        if mode in ["Channel Videos", "Channel Videos MP3"]:
            if not url.lower().rstrip("/").endswith("/videos"):
                url = url.rstrip("/") + "/videos"
        elif mode in ["Channel Shorts", "Channel Shorts MP3"]:
            if not url.lower().rstrip("/").endswith("/shorts"):
                url = url.rstrip("/") + "/shorts"
        try:
            opts = {"quiet": True, "extract_flat": True}
            with yt_dlp.YoutubeDL(opts) as ydl:
                channel_info = ydl.extract_info(url, download=False)
            if "entries" not in channel_info:
                QMessageBox.critical(self, "Error", "No videos found for channel.")
                return
            entries = channel_info["entries"]
            if mode in ["Channel Videos", "Channel Videos MP3"]:
                filtered = [
                    entry
                    for entry in entries
                    if entry and ("shorts" not in entry.get("url", "").lower())
                ]
            else:
                filtered = [
                    entry
                    for entry in entries
                    if entry and ("shorts" in entry.get("url", "").lower())
                ]
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to extract channel info: {e}")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Select Videos from Channel")
        dialog.resize(600, 400)
        dlg_layout = QVBoxLayout()
        dialog.setLayout(dlg_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        dlg_layout.addWidget(scroll_area)
        container = QWidget()
        scroll_layout = QVBoxLayout()
        container.setLayout(scroll_layout)
        scroll_area.setWidget(container)

        self.channel_checkboxes = []
        for entry in filtered:
            video_url = entry.get("url")
            if video_url and not video_url.startswith("http"):
                video_url = channel_info.get("webpage_url", "") + video_url
            title = entry.get("title", "Unknown Title")
            checkbox = QCheckBox(title)
            if self.video_favicon_pixmap:
                checkbox.setIcon(QIcon(self.video_favicon_pixmap))
            checkbox.setChecked(True)
            scroll_layout.addWidget(checkbox)
            self.channel_checkboxes.append((video_url, title, checkbox))

        download_btn = QPushButton("Download Selected")
        dlg_layout.addWidget(download_btn)

        def download_selected():
            count = 0
            for video_url, title, checkbox in self.channel_checkboxes:
                if checkbox.isChecked():
                    task = {
                        "url": video_url,
                        "save_path": save_path,
                        "mode": mode,
                        "audio_quality": (
                            self.audio_quality_default if "MP3" in mode else None
                        ),
                        "video_quality": (
                            self.video_quality_combo.currentText()
                            if mode in ["Channel Videos", "Channel Shorts"]
                            else "Best Available"
                        ),
                    }
                    self.download_queue.append(task)
                    count += 1
            if count == 0:
                QMessageBox.information(dialog, "Info", "No videos selected.")
            else:
                self.log_message(f"{count} videos added to queue from channel.")
                self.process_queue()
            dialog.accept()

        download_btn.clicked.connect(download_selected)
        dialog.exec()

    def create_activity_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        page.setLayout(layout)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)
        return page

    def process_queue(self):
        if not self.downloading and self.download_queue:
            task = self.download_queue.pop(0)
            self.downloading = True
            self.download_thread = threading.Thread(
                target=self.download_video, args=(task,), daemon=True
            )
            self.download_thread.start()

    def download_video(self, task):
        url = task["url"]
        save_path = task["save_path"]
        mode = task["mode"]
        video_quality = task.get("video_quality", "Best Available")
        self.update_status(f"Starting download: {url}")
        if mode in [
            "Single Video",
            "Playlist Video",
            "Channel Videos",
            "Channel Shorts",
        ]:
            ydl_opts = {
                "outtmpl": os.path.join(save_path, "%(title)s.%(ext)s"),
                "ffmpeg_location": os.path.join(self.base_dir, "bin", "ffmpeg.exe"),
                "noplaylist": True,
                "progress_hooks": [self.update_progress],
                "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
                "merge_output_format": "mp4",
            }
            if video_quality != "Best Available":
                height = video_quality.split("p")[0]
                ydl_opts["format"] = (
                    f"bestvideo[ext=mp4][height<={height}]+bestaudio[ext=m4a]/mp4"
                )
        elif mode in [
            "MP3 Only",
            "Playlist MP3",
            "Channel Videos MP3",
            "Channel Shorts MP3",
        ]:
            ydl_opts = {
                "outtmpl": os.path.join(save_path, "%(title)s.%(ext)s"),
                "ffmpeg_location": os.path.join(self.base_dir, "bin", "ffmpeg.exe"),
                "noplaylist": True,
                "progress_hooks": [self.update_progress],
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": self.audio_quality_default,
                    }
                ],
            }
        else:
            QMessageBox.critical(self, "Error", "Invalid download mode.")
            self.downloading = False
            return

        # If login was used, add cookiesfrombrowser option using the chosen browser
        if self.use_cookies:
            ydl_opts["cookiesfrombrowser"] = (self.cookie_browser,)
            self.log_message("Login successful, using cookies from browser.")

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get("title", "Unknown")
                self.log_message(f"Downloading: {title}")
                ydl.download([url])
                self.log_message(f"Download completed: {title}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Download failed: {e}")
            self.log_message("Download failed")
        finally:
            self.downloading = False
            self.process_queue()

    def update_progress(self, d):
        if d["status"] == "downloading":
            percent_str = d.get("_percent_str", "0%").strip()
            speed = d.get("_speed_str", "0 KB/s").strip()
            self.log_message(
                f"{d['info_dict'].get('title','Unknown')} - {percent_str} at {speed}"
            )
        elif d["status"] == "finished":
            self.log_message(
                f"{d['info_dict'].get('title','Unknown')} - Download finished."
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SSTubeGUI()
    window.show()
    sys.exit(app.exec())
