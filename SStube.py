import os
import sys
import threading
import webbrowser
import json
import urllib.request
import shutil
import stat
import subprocess

import yt_dlp
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

class Updater:
    YTDLP_RELEASES = "https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest"

    def __init__(self, base_dir, parent=None):
        self.base_dir = base_dir
        self.parent = parent
        self.yt_dlp_path = os.path.join(base_dir, "bin", "yt-dlp.exe")

    def get_latest_yt_version(self):
        with urllib.request.urlopen(self.YTDLP_RELEASES) as resp:
            data = json.load(resp)
        version = data.get("tag_name", "").lstrip("release/")
        assets = data.get("assets", [])
        return version, assets

    def download_yt(self, progress_callback):
        version, assets = self.get_latest_yt_version()
        exe_asset = next((a for a in assets if a["name"].endswith(".exe")), None)
        if not exe_asset:
            progress_callback("No yt-dlp executable found in release assets.")
            return
        url = exe_asset["browser_download_url"]
        target = self.yt_dlp_path
        progress_callback(f"Downloading yt-dlp {version}...")
        # download to temp then replace
        temp_path = target + ".new"
        with urllib.request.urlopen(url) as r, open(temp_path, "wb") as f:
            shutil.copyfileobj(r, f)
        os.replace(temp_path, target)
        os.chmod(target, stat.S_IEXEC | stat.S_IREAD | stat.S_IWRITE)
        progress_callback(f"yt-dlp updated to {version} at {target}")


class SSTubeGUI(QMainWindow):
    updateStatusSignal = pyqtSignal(str)
    logMessageSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SSTube")
        self.resize(400, 300)

        # Determine base directory
        if getattr(sys, "frozen", False):
            self.base_dir = os.path.dirname(sys.executable)
        else:
            self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # Initialize updater
        self.updater = Updater(self.base_dir, parent=self)

        # Window icon
        try:
            icon_path = os.path.join(self.base_dir, "Favicon.png")
            self.setWindowIcon(QIcon(icon_path))
        except Exception:
            pass

        # Download queue and state
        self.download_queue = []
        self.downloading = False
        self.audio_quality_default = "320"
        self.use_cookies = False
        self.cookie_browser = "chrome"
        self.cookie_file = None

        # Icons
        self.icons = {
            "download": self.load_icon(os.path.join(self.base_dir, "assets", "download.png")),
            "activity": self.load_icon(os.path.join(self.base_dir, "assets", "activity.png")),
        }
        # Video favicon
        try:
            vf_path = os.path.join(self.base_dir, "assets", "video-favicon.png")
            self.video_favicon_pixmap = (
                QPixmap(vf_path)
                .scaled(16, 16, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            )
        except Exception:
            self.video_favicon_pixmap = None

        self.create_menubar()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        # Sidebar
        self.sidebar = self.create_sidebar()
        layout.addWidget(self.sidebar)

        # Pages
        from PyQt6.QtWidgets import QStackedWidget
        self.stack = QStackedWidget()
        self.download_page = self.create_download_page()
        self.activity_page = self.create_activity_page()
        self.stack.addWidget(self.download_page)
        self.stack.addWidget(self.activity_page)
        layout.addWidget(self.stack, 1)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.updateStatusSignal.connect(self._update_status)
        self.logMessageSignal.connect(self._log_message)
        self.update_status("Ready")

        # Startup update check
        QTimer.singleShot(100, self.check_for_updates)

    def load_icon(self, path):
        try:
            return QIcon(QPixmap(path))
        except Exception:
            return QIcon()

    def create_menubar(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        login_action = QAction("Login", self)
        login_action.triggered.connect(self.open_login)
        file_menu.addAction(login_action)

        help_menu = menubar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def check_for_updates(self):
        reply = QMessageBox.question(
            self, "Check for Updates",
            "Do you want to check for a new version of yt-dlp?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.switch_page("Activity")
            threading.Thread(target=self.run_updates, daemon=True).start()

    def run_updates(self):
        def progress_callback(msg):
            self.log_message(msg)

        self.log_message("Starting yt-dlp update...")
        try:
            self.updater.download_yt(progress_callback)
            self.log_message("yt-dlp update completed.")
        except Exception as e:
            self.log_message(f"Update error: {e}")
            QTimer.singleShot(0, lambda: QMessageBox.critical(self, "Updater", f"Error during yt-dlp update: {e}"))

    def get_installed_browsers(self):
        try:
            import winreg

            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Clients\StartMenuInternet"
            )
            i, browsers = 0, []
            while True:
                try:
                    browsers.append(winreg.EnumKey(key, i))
                    i += 1
                except OSError:
                    break
            return browsers or ["Google Chrome", "Mozilla Firefox", "Microsoft Edge"]
        except Exception:
            return ["Google Chrome", "Mozilla Firefox", "Microsoft Edge"]

    def map_browser(self, browser_name):
        name = browser_name.lower()
        return (
            "chrome"
            if "chrome" in name
            else "firefox"
            if "firefox" in name
            else "edge"
            if "edge" in name
            else "opera"
            if "opera" in name
            else "brave"
            if "brave" in name
            else name
        )

    def open_login(self):
        if self.use_cookies:
            QMessageBox.information(self, "Login", "Already logged in.")
            return

        installed = self.get_installed_browsers()
        browser_choice, ok = QInputDialog.getItem(
            self, "Select Browser", "Select your browser:", installed, 0, False
        )
        if not ok:
            return
        self.cookie_browser = self.map_browser(browser_choice)

        reply = QMessageBox.question(
            self,
            "Cookie Extension",
            "Have you installed the 'Get cookies.txt Locally' extension?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        browser_paths = {
            "chrome": r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
            "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            "opera": r"C:\Program Files\Opera\launcher.exe",
            "brave": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        }
        exe_path = browser_paths.get(self.cookie_browser)

        if reply == QMessageBox.StandardButton.Yes:
            cookie_file, _ = QFileDialog.getOpenFileName(
                self, "Select Cookie File", "", "Text Files (*.txt);;All Files (*)"
            )
            if cookie_file:
                try:
                    with open(cookie_file, "r", encoding="utf-8", errors="ignore") as f:
                        data = f.read()
                    if "youtube.com" in data.lower():
                        self.cookie_file = cookie_file
                        self.use_cookies = True
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Cannot read file: {e}")
        else:
            ext_url = (
                "https://chromewebstore.google.com/detail/"
                "get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc"
            )
            if exe_path and os.path.exists(exe_path):
                webbrowser.BackgroundBrowser(exe_path).open(ext_url)
            else:
                webbrowser.open(ext_url)
            QMessageBox.information(self, "Cookie Extension", "Please install it, then select the file.")
            cookie_file, _ = QFileDialog.getOpenFileName(
                self, "Select Cookie File", "", "Text Files (*.txt);;All Files (*)"
            )
            if cookie_file:
                try:
                    with open(cookie_file, "r", encoding="utf-8", errors="ignore") as f:
                        data = f.read()
                    if "youtube.com" in data.lower():
                        self.cookie_file = cookie_file
                        self.use_cookies = True
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Cannot read file: {e}")

        if not self.use_cookies:
            return

        # Open YouTube login to confirm
        login_url = "https://accounts.google.com/ServiceLogin?service=youtube"
        if exe_path and os.path.exists(exe_path):
            webbrowser.BackgroundBrowser(exe_path).open(login_url)
        else:
            webbrowser.open(login_url)
        QMessageBox.information(self, "Login", "Log in in the browser, then click OK.")

    def show_about(self):
        QMessageBox.information(
            self,
            "About SSTube",
            "SSTube Video Downloader\nVersion 2.1.0\nDeveloped by UKR\nReport bugs via our support channel.",
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
        widget = QWidget()
        layout = QVBoxLayout(widget)
        header = QLabel("SSTube")
        header.setStyleSheet("font-size: 16pt; font-weight: bold;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        layout.addSpacing(20)
        for name in ("Download", "Activity"):
            btn = QPushButton(name)
            icon = self.icons.get(name.lower())
            if icon:
                btn.setIcon(icon)
                btn.setIconSize(QSize(32, 32))
            btn.clicked.connect(lambda _, n=name: self.switch_page(n))
            layout.addWidget(btn)
        layout.addStretch()
        return widget

    def switch_page(self, name):
        if name == "Download":
            self.stack.setCurrentWidget(self.download_page)
        else:
            self.stack.setCurrentWidget(self.activity_page)
        self.update_status(f"{name} section active")

    def create_download_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Enter YouTube URL (or Playlist/Channel URL):", styleSheet="font-size: 12pt;"))

        self.url_entry = QLineEdit()
        self.url_entry.setPlaceholderText("Enter URL here")
        layout.addWidget(self.url_entry)

        layout.addWidget(QLabel("Save Location:", styleSheet="font-size: 12pt;"))
        path_layout = QHBoxLayout()
        self.path_entry = QLineEdit(readOnly=True)
        path_layout.addWidget(self.path_entry)
        browse_btn = QPushButton("Browse Folder")
        browse_btn.clicked.connect(self.select_save_path)
        path_layout.addWidget(browse_btn)
        layout.addLayout(path_layout)

        layout.addWidget(QLabel("Download Mode:", styleSheet="font-size: 12pt;"))
        self.mode_combo = QComboBox()
        modes = [
            "Single Video", "MP3 Only",
            "Playlist Video", "Playlist MP3",
            "Channel Videos", "Channel Videos MP3",
            "Channel Shorts", "Channel Shorts MP3",
        ]
        self.mode_combo.addItems(modes)
        self.mode_combo.currentTextChanged.connect(self.mode_changed)
        layout.addWidget(self.mode_combo)

        self.video_quality_label = QLabel("Video Quality:")
        self.video_quality_combo = QComboBox()
        self.video_quality_combo.addItems(
            ["Best Available", "4320p 8K", "2160p 4K", "1440p 2K", "1080p Full HD", "720p HD", "480p Standard", "360p Medium"]
        )
        layout.addWidget(self.video_quality_label)
        layout.addWidget(self.video_quality_combo)
        self.mode_changed(self.mode_combo.currentText())

        download_btn = QPushButton("Download")
        download_btn.clicked.connect(self.add_to_queue)
        layout.addWidget(download_btn)
        layout.addStretch()
        return page

    def mode_changed(self, text):
        self.mode_var = text
        if "MP3" in text:
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
            QMessageBox.critical(self, "Error", "Please enter a URL and select a save path.")
            return

        # URL validation per mode...
        if mode in ["Playlist Video", "Playlist MP3"]:
            if "list=" not in url:
                QMessageBox.critical(self, "Error", "The URL does not appear to be a playlist.")
                return
            return self.process_playlist(url, save_path, mode)
        if mode in ["Channel Videos", "Channel Videos MP3", "Channel Shorts", "Channel Shorts MP3"]:
            if "youtube.com/@" not in url and "/channel/" not in url:
                QMessageBox.critical(self, "Error", "The URL does not appear to be a channel.")
                return
            if "?" in url:
                QMessageBox.critical(self, "Error", "Please use a clean channel URL without query parameters.")
                return
            return self.process_channel(url, save_path, mode)

        # Single video or MP3 Only
        task = {
            "url": url,
            "save_path": save_path,
            "mode": mode,
            "audio_quality": self.audio_quality_default if "MP3" in mode else None,
            "video_quality": self.video_quality_combo.currentText() if "MP3" not in mode else "Best Available",
        }
        self.download_queue.append(task)
        self.log_message("Task added to queue")
        self.process_queue()

    def process_playlist(self, url, save_path, mode):
        try:
            with yt_dlp.YoutubeDL({"quiet": True, "extract_flat": True}) as ydl:
                info = ydl.extract_info(url, download=False)
            entries = info.get("entries") or []
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to extract playlist info: {e}")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Select Videos from Playlist")
        dlg_layout = QVBoxLayout(dialog)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        dlg_layout.addWidget(scroll)
        container = QWidget()
        scroll.setWidget(container)
        scroll_layout = QVBoxLayout(container)

        checkboxes = []
        for entry in entries:
            video_url = entry.get("url")
            if video_url and not video_url.startswith("http"):
                video_url = info.get("webpage_url", "") + video_url
            cb = QCheckBox(entry.get("title", "Unknown Title"))
            if self.video_favicon_pixmap:
                cb.setIcon(QIcon(self.video_favicon_pixmap))
            cb.setChecked(True)
            scroll_layout.addWidget(cb)
            checkboxes.append((video_url, cb))

        def dl_sel():
            for video_url, cb in checkboxes:
                if cb.isChecked():
                    self.download_queue.append({
                        "url": video_url,
                        "save_path": save_path,
                        "mode": mode,
                        "audio_quality": self.audio_quality_default if "MP3" in mode else None,
                        "video_quality": self.video_quality_combo.currentText() if "Video" in mode else "Best Available",
                    })
            self.process_queue()
            dialog.accept()

        btn = QPushButton("Download Selected")
        btn.clicked.connect(dl_sel)
        dlg_layout.addWidget(btn)
        dialog.exec()

    def process_channel(self, url, save_path, mode):
        suffix = "/videos" if "Videos" in mode else "/shorts"
        if not url.lower().endswith(suffix):
            url = url.rstrip("/") + suffix
        try:
            with yt_dlp.YoutubeDL({"quiet": True, "extract_flat": True}) as ydl:
                info = ydl.extract_info(url, download=False)
            entries = info.get("entries") or []
            if "Shorts" in mode:
                entries = [e for e in entries if "shorts" in e.get("url", "").lower()]
            else:
                entries = [e for e in entries if "shorts" not in e.get("url", "").lower()]
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to extract channel info: {e}")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Select Videos from Channel")
        dlg_layout = QVBoxLayout(dialog)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        dlg_layout.addWidget(scroll)
        container = QWidget()
        scroll.setWidget(container)
        scroll_layout = QVBoxLayout(container)

        checkboxes = []
        for entry in entries:
            video_url = entry.get("url")
            if video_url and not video_url.startswith("http"):
                video_url = info.get("webpage_url", "") + video_url
            cb = QCheckBox(entry.get("title", "Unknown Title"))
            if self.video_favicon_pixmap:
                cb.setIcon(QIcon(self.video_favicon_pixmap))
            cb.setChecked(True)
            scroll_layout.addWidget(cb)
            checkboxes.append((video_url, cb))

        def dl_sel():
            for video_url, cb in checkboxes:
                if cb.isChecked():
                    self.download_queue.append({
                        "url": video_url,
                        "save_path": save_path,
                        "mode": mode,
                        "audio_quality": self.audio_quality_default if "MP3" in mode else None,
                        "video_quality": self.video_quality_combo.currentText() if "Videos" in mode or "Shorts" in mode else "Best Available",
                    })
            self.process_queue()
            dialog.accept()

        btn = QPushButton("Download Selected")
        btn.clicked.connect(dl_sel)
        dlg_layout.addWidget(btn)
        dialog.exec()

    def create_activity_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        self.log_text = QTextEdit(readOnly=True)
        layout.addWidget(self.log_text)
        return page

    def process_queue(self):
        if not self.downloading and self.download_queue:
            task = self.download_queue.pop(0)
            self.downloading = True
            threading.Thread(target=self.download_video, args=(task,), daemon=True).start()

    def download_video(self, task):
        url = task["url"]
        save_path = task["save_path"]
        mode = task["mode"]
        vq = task.get("video_quality", "Best Available")

        self.update_status(f"Starting download: {url}")
        if "Video" in mode and "MP3" not in mode:
            opts = {
                "outtmpl": os.path.join(save_path, "%(title)s.%(ext)s"),
                "ffmpeg_location": os.path.join(self.base_dir, "bin", "ffmpeg.exe"),
                "noplaylist": True,
                "progress_hooks": [self.update_progress],
                "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
                "merge_output_format": "mp4",
            }
            if vq != "Best Available":
                h = vq.split("p")[0]
                opts["format"] = f"bestvideo[height<={h}]+bestaudio/merge"
        else:
            opts = {
                "outtmpl": os.path.join(save_path, "%(title)s.%(ext)s"),
                "ffmpeg_location": os.path.join(self.base_dir, "bin", "ffmpeg.exe"),
                "noplaylist": True,
                "progress_hooks": [self.update_progress],
                "format": "bestaudio/best",
                "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": self.audio_quality_default}],
            }

        if self.use_cookies and self.cookie_file:
            opts["cookiefile"] = self.cookie_file
            self.log_message("Using cookie file for downloads.")

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get("title", "Unknown")
                self.log_message(f"Downloading: {title}")
                ydl.download([url])
                self.log_message(f"Download completed: {title}")
        except Exception as e:
            QTimer.singleShot(
                0,
                lambda: QMessageBox.critical(
                    self,
                    "Error",
                    f"Download failed: {e}\n\n"
                    "If you see 'Failed to decrypt with DPAPI', ensure:\n"
                    "- Run under the same user as Chrome.\n"
                    "- Chrome is closed before downloading.\n"
                    "- Or export cookies manually.",
                ),
            )
            self.log_message("Download failed")
        finally:
            self.downloading = False
            self.process_queue()

    def update_progress(self, d):
        if d["status"] == "downloading":
            self.log_message(f"{d['info_dict'].get('title','')} - {d.get('_percent_str','')} at {d.get('_speed_str','')}")
        elif d["status"] == "finished":
            self.log_message(f"{d['info_dict'].get('title','')} - Download finished.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SSTubeGUI()
    window.show()
    sys.exit(app.exec())
