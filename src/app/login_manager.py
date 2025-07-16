"""
Handles user login and cookie-based authentication.
"""

import os
import webbrowser
from typing import List, Optional

from PyQt6.QtWidgets import QMessageBox, QInputDialog, QFileDialog


class LoginManager:
    """Handles user login and cookie-based authentication."""

    def __init__(self, main_app: "YTDGUI"):
        self.main_app = main_app

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
                winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Clients\StartMenuInternet"
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
            "brave": "brave",
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
        if self.main_app.use_cookies:
            QMessageBox.information(self.main_app, "Login", "Already logged in.")
            return

        # Get user's browser preference
        installed_browsers = self.get_installed_browsers()
        browser_choice, ok = QInputDialog.getItem(
            self.main_app,
            "Select Browser",
            "Select your browser:",
            installed_browsers,
            0,
            False,
        )

        if not ok:
            return

        self.main_app.cookie_browser = self.map_browser(browser_choice)

        # Check if user has cookie extension installed
        reply = QMessageBox.question(
            self.main_app,
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

        exe_path = browser_paths.get(self.main_app.cookie_browser)

        if reply == QMessageBox.StandardButton.Yes:
            # User has extension, let them select cookie file
            self._handle_cookie_file_selection()
        else:
            # User doesn't have extension, guide them to install it
            self._guide_extension_installation(exe_path)

        # If login was successful, open YouTube login page
        if self.main_app.use_cookies:
            self._open_youtube_login(exe_path)

    def _handle_cookie_file_selection(self) -> None:
        """Handle cookie file selection dialog."""
        cookie_file, _ = QFileDialog.getOpenFileName(
            self.main_app, "Select Cookie File", "", "Text Files (*.txt);;All Files (*)"
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
            self.main_app,
            "Cookie Extension",
            "Please install the extension, then select the cookie file.",
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
                self.main_app.cookie_file = cookie_file
                self.main_app.use_cookies = True
                self.main_app.log_message(f"Cookie file set: {cookie_file}")
            else:
                QMessageBox.warning(
                    self.main_app,
                    "Invalid Cookie File",
                    "The selected file doesn't appear to contain YouTube cookies.",
                )
        except Exception as e:
            QMessageBox.warning(self.main_app, "Error", f"Cannot read cookie file: {e}")

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
            self.main_app,
            "Login",
            "Please log in to YouTube in the browser, then click OK.",
        )
