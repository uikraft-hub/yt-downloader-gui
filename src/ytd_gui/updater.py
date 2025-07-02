"""
Handles automatic updates for the yt-dlp binary.
"""

import os
import json
import urllib.request
import shutil
import stat
from typing import Dict, List, Optional, Callable, Tuple

from PyQt6.QtWidgets import QWidget


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
        self.yt_dlp_path = os.path.join(self.base_dir, "bin", "yt-dlp.exe")

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
