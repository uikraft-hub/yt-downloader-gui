"""
Handles the download queue and execution.
"""

import os
import re
import threading
import subprocess
import json
import sys
from typing import Dict, List, Any, Tuple, TYPE_CHECKING, Optional

from PyQt6.QtWidgets import (
    QMessageBox,
    QDialog,
    QScrollArea,
    QWidget,
    QVBoxLayout,
    QLabel,
    QCheckBox,
    QHBoxLayout,
    QPushButton,
)
from PyQt6.QtCore import QTimer, pyqtSignal, QObject
from PyQt6.QtGui import QIcon

if TYPE_CHECKING:
    from .main_window import YTDGUI


class WorkerSignals(QObject):
    """Defines signals available from a running worker thread."""

    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)


class DownloadManager:
    """Handles the download queue and execution."""

    def __init__(self, main_app: "YTDGUI"):
        self.main_app = main_app
        self.signals = WorkerSignals()
        self.signals.error.connect(self._on_playlist_error)
        self.signals.result.connect(self._on_playlist_result)

    def _on_playlist_error(self, error_info: tuple) -> None:
        """Handles errors from the playlist processing thread."""
        exctype, value = error_info
        QMessageBox.critical(
            self.main_app, "Error", f"Failed to extract playlist information: {value}"
        )

    def _on_playlist_result(self, result: Any) -> None:
        """Handles successful results from the playlist processing thread."""
        entries, save_path, mode, title = result
        if not entries:
            QMessageBox.warning(
                self.main_app, "Warning", "No videos found in the playlist."
            )
            return
        self._show_video_selection_dialog(entries, save_path, mode, title)

    def add_to_queue(self) -> None:
        """
        Validate input and add download task to queue.

        This method handles different download modes and validates URLs
        before adding tasks to the download queue.
        """
        # Get and validate input
        url = self.main_app.url_entry.text().strip()
        save_path = self.main_app.path_entry.text().strip()
        mode = self.main_app.mode_combo.currentText()

        if not url or not save_path:
            QMessageBox.critical(
                self.main_app, "Error", "Please enter a URL and select a save path."
            )
            return

        # Handle different download modes
        if mode in ["Playlist Video", "Playlist MP3"]:
            self._handle_playlist_download(url, save_path, mode)
        elif mode in [
            "Channel Videos",
            "Channel Videos MP3",
            "Channel Shorts",
            "Channel Shorts MP3",
        ]:
            self._handle_channel_download(url, save_path, mode)
        else:
            # Single video or MP3 only
            self._handle_single_download(url, save_path, mode)

    def _handle_playlist_download(self, url: str, save_path: str, mode: str) -> None:
        """Handle playlist download mode."""
        if "list=" not in url:
            QMessageBox.critical(
                self.main_app,
                "Error",
                "The URL does not appear to be a playlist URL.\n"
                "Playlist URLs should contain 'list=' parameter.",
            )
            return
        threading.Thread(
            target=self.process_playlist, args=(url, save_path, mode), daemon=True
        ).start()

    def _handle_channel_download(self, url: str, save_path: str, mode: str) -> None:
        """Handle channel download mode."""
        if "youtube.com/@" not in url and "/channel/" not in url:
            QMessageBox.critical(
                self.main_app,
                "Error",
                "The URL does not appear to be a channel URL.\n"
                "Channel URLs should contain '@' or '/channel/'.",
            )
            return
        if "?" in url:
            QMessageBox.critical(
                self.main_app,
                "Error",
                "Please use a clean channel URL without query parameters.\n"
                "Example: https://www.youtube.com/@channelname",
            )
            return
        threading.Thread(
            target=self.process_channel, args=(url, save_path, mode), daemon=True
        ).start()

    def _handle_single_download(self, url: str, save_path: str, mode: str) -> None:
        """Handle single video or MP3-only download."""
        # Create download task
        task = {
            "url": url,
            "save_path": save_path,
            "mode": mode,
            "audio_quality": (
                self.main_app.audio_quality_default if "MP3" in mode else None
            ),
            "video_quality": (
                self.main_app.video_quality_combo.currentText()
                if "MP3" not in mode
                else "Best Available"
            ),
        }

        self.main_app.download_queue.append(task)
        self.main_app.log_message(f"Task added to queue: {mode}")
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
            yt_dlp_path = os.path.join(self.main_app.base_dir, "bin", "yt-dlp.exe")
            cmd = [yt_dlp_path, "--quiet", "--flat-playlist", "--dump-json", url]

            creationflags = 0
            if sys.platform == "win32":
                creationflags = subprocess.CREATE_NO_WINDOW

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                creationflags=creationflags,
            )

            entries = []
            for line in result.stdout.strip().split("\n"):
                if line.strip():
                    try:
                        entry = json.loads(line)
                        entries.append(entry)
                    except json.JSONDecodeError:
                        continue

            if not entries:
                QMessageBox.warning(
                    self.main_app, "Warning", "No videos found in the playlist."
                )
                return

        except Exception as e:
            QMessageBox.critical(
                self.main_app, "Error", f"Failed to extract playlist information: {e}"
            )
            return

        # Show video selection dialog
        self.signals.result.emit(
            (entries, save_path, mode, "Select Videos from Playlist")
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
            yt_dlp_path = os.path.join(self.main_app.base_dir, "bin", "yt-dlp.exe")
            cmd = [yt_dlp_path, "--quiet", "--flat-playlist", "--dump-json", url]

            creationflags = 0
            if sys.platform == "win32":
                creationflags = subprocess.CREATE_NO_WINDOW

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                creationflags=creationflags,
            )

            entries = []
            for line in result.stdout.strip().split("\n"):
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
                entries = [
                    e for e in entries if "shorts" not in e.get("url", "").lower()
                ]

            if not entries:
                content_type = "shorts" if "Shorts" in mode else "videos"
                QMessageBox.warning(
                    self.main_app, "Warning", f"No {content_type} found in the channel."
                )
                return

        except Exception as e:
            QMessageBox.critical(
                self.main_app, "Error", f"Failed to extract channel information: {e}"
            )
            return

        # Show video selection dialog
        dialog_title = (
            "Select Videos from Channel"
            if "Videos" in mode
            else "Select Shorts from Channel"
        )
        self.signals.result.emit((entries, save_path, mode, dialog_title))

    def _show_video_selection_dialog(
        self, entries: List[Dict], save_path: str, mode: str, title: str
    ) -> None:
        """
        Show dialog for selecting videos from playlist or channel.

        Args:
            entries: List of video entries
            save_path: Download destination path
            mode: Download mode
            title: Dialog window title
        """
        dialog = QDialog(self.main_app)
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
            if self.main_app.video_favicon_pixmap:
                cb.setIcon(QIcon(self.main_app.video_favicon_pixmap))

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

    def _process_selected_videos(
        self, checkboxes: List[Tuple], save_path: str, mode: str, dialog: QDialog
    ) -> None:
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
                    "audio_quality": (
                        self.main_app.audio_quality_default if "MP3" in mode else None
                    ),
                    "video_quality": (
                        self.main_app.video_quality_combo.currentText()
                        if "MP3" not in mode
                        else "Best Available"
                    ),
                }
                self.main_app.download_queue.append(task)
                selected_count += 1

        if selected_count == 0:
            QMessageBox.warning(dialog, "Warning", "No videos selected for download.")
            return

        # Log and start processing
        self.main_app.log_message(f"Added {selected_count} videos to download queue")
        dialog.accept()

        # Switch to activity page and start downloads
        self.main_app.ui_manager.switch_page("Activity")
        self.process_queue()

    def process_queue(self) -> None:
        """
        Process the download queue by starting the next download.

        This method ensures only one download runs at a time and automatically
        processes the next item in the queue when the current download completes.
        """
        # Update queue status
        if hasattr(self.main_app, "queue_status_label"):
            self.main_app.queue_status_label.setText(
                f"Queue: {len(self.main_app.download_queue)} pending"
            )

        # Start next download if not already downloading and queue has items
        if not self.main_app.downloading and self.main_app.download_queue:
            task = self.main_app.download_queue.pop(0)
            self.main_app.downloading = True

            # Start download in background thread
            threading.Thread(
                target=self.download_video, args=(task,), daemon=True
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

        self.main_app.update_status(f"Starting download: {os.path.basename(url)}")

        try:
            # Get yt-dlp.exe path
            yt_dlp_path = os.path.join(self.main_app.base_dir, "bin", "yt-dlp.exe")
            ffmpeg_path = os.path.join(self.main_app.base_dir, "bin", "ffmpeg.exe")

            # Build command based on mode
            if "Video" in mode and "MP3" not in mode:
                # Video download
                cmd = self._build_video_download_command(
                    yt_dlp_path, ffmpeg_path, url, save_path, video_quality
                )
            else:
                # Audio extraction
                cmd = self._build_audio_download_command(
                    yt_dlp_path,
                    ffmpeg_path,
                    url,
                    save_path,
                    task.get("audio_quality", "320"),
                )

            # Add cookie support if enabled
            if self.main_app.use_cookies and self.main_app.cookie_file:
                cmd.extend(["--cookies", self.main_app.cookie_file])
                self.main_app.log_message("Using cookie file for authentication")

            # Get video info first for logging
            info_cmd = [yt_dlp_path, "--quiet", "--dump-json", "--no-playlist", url]
            if self.main_app.use_cookies and self.main_app.cookie_file:
                info_cmd.extend(["--cookies", self.main_app.cookie_file])

            try:
                creationflags = 0
                if sys.platform == "win32":
                    creationflags = subprocess.CREATE_NO_WINDOW
                info_result = subprocess.run(
                    info_cmd,
                    capture_output=True,
                    text=True,
                    check=True,
                    creationflags=creationflags,
                )
                info = json.loads(info_result.stdout)
                title = info.get("title", "Unknown Title")
            except:
                title = "Unknown Title"

            self.main_app.log_message(f"Starting download: {title}")

            # Execute download command
            creationflags = 0
            if sys.platform == "win32":
                creationflags = subprocess.CREATE_NO_WINDOW
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                universal_newlines=True,
                creationflags=creationflags,
            )

            # Read output line by line for progress updates
            if process.stdout:
                for line in iter(process.stdout.readline, ""):
                    line = line.strip()
                    if line:
                        self.main_app.log_message(line)
                        progress = self._parse_progress(line)
                        if progress is not None:
                            self.main_app.updateProgressSignal.emit(progress)

            process.wait()

            # Check if download was successful
            if process.returncode == 0:
                self.main_app.log_message(f"Download completed: {title}")
            else:
                raise subprocess.CalledProcessError(process.returncode, cmd)

        except Exception as e:
            error_msg = f"Download failed for {url}: {str(e)}"
            self.main_app.log_message(error_msg)

            # Show detailed error dialog in main thread
            QTimer.singleShot(0, lambda e=e: self._show_download_error(e))

        finally:
            # Mark download as complete and process next in queue
            self.main_app.downloading = False
            self.main_app.updateProgressSignal.emit(0)  # Reset progress bar
            QTimer.singleShot(100, self.process_queue)  # Small delay to update UI

    def _parse_progress(self, line: str) -> Optional[int]:
        """
        Parse download progress from yt-dlp output line.

        Args:
            line: A single line of output from yt-dlp.

        Returns:
            The progress percentage as an integer, or None if not found.
        """
        # Look for percentage values (e.g., "  1.5% of ...")
        match = re.search(r"\[download\]\s+([0-9.]+)%", line)
        if match:
            try:
                return int(float(match.group(1)))
            except (ValueError, IndexError):
                pass
        return None

    def _build_video_download_command(
        self,
        yt_dlp_path: str,
        ffmpeg_path: str,
        url: str,
        save_path: str,
        video_quality: str,
    ) -> List[str]:
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
            "--ffmpeg-location",
            ffmpeg_path,
            "--no-playlist",
            "--output",
            os.path.join(save_path, "%(title)s.%(ext)s"),
            "--format",
            "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
            "--merge-output-format",
            "mp4",
            url,
        ]

        # Apply quality filter if not "Best Available"
        if video_quality != "Best Available":
            height = video_quality.split("p")[0]
            cmd[cmd.index("--format") + 1] = (
                f"bestvideo[height<={height}]+bestaudio/merge"
            )

        return cmd

    def _build_audio_download_command(
        self,
        yt_dlp_path: str,
        ffmpeg_path: str,
        url: str,
        save_path: str,
        audio_quality: str,
    ) -> List[str]:
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
            "--ffmpeg-location",
            ffmpeg_path,
            "--no-playlist",
            "--output",
            os.path.join(save_path, "%(title)s.%(ext)s"),
            "--format",
            "bestaudio/best",
            "--extract-audio",
            "--audio-format",
            "mp3",
            "--audio-quality",
            audio_quality,
            url,
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
                "• Run yt-downloader-gui as the same user who uses Chrome\n"
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
            self.main_app, "Download Error", f"Download failed:\n\n{error_text}"
        )
