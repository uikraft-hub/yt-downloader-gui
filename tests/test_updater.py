import os
import sys
import unittest
import json
from unittest.mock import patch, mock_open, MagicMock

# Add the 'src' directory to the Python path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from app.updater import Updater


class TestUpdater(unittest.TestCase):
    """Tests for the Updater class."""

    def setUp(self):
        """Set up the test environment."""
        self.base_dir = "/fake/base/dir"
        self.updater = Updater(self.base_dir)
        self.mock_api_response = {
            "tag_name": "2023.12.30",
            "assets": [
                {
                    "name": "yt-dlp.exe",
                    "browser_download_url": "https://fake.url/yt-dlp.exe",
                },
                {"name": "yt-dlp", "browser_download_url": "https://fake.url/yt-dlp"},
            ],
        }

    @patch("urllib.request.urlopen")
    def test_get_latest_yt_version_success(self, mock_urlopen):
        """Test successfully fetching the latest version from the GitHub API."""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(self.mock_api_response).encode()
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        version, assets = self.updater.get_latest_yt_version()

        self.assertEqual(version, "2023.12.30")
        self.assertEqual(len(assets), 2)
        self.assertEqual(assets[0]["name"], "yt-dlp.exe")

    @patch("app.updater.Updater.get_latest_yt_version")
    @patch("urllib.request.urlopen")
    @patch("shutil.copyfileobj")
    @patch("os.replace")
    @patch("os.chmod")
    @patch("builtins.open", new_callable=mock_open)
    def test_download_yt_success(
        self,
        mock_file,
        mock_chmod,
        mock_replace,
        mock_copy,
        mock_urlopen,
        mock_get_version,
    ):
        """Test the full download and replacement process."""
        # Mock the necessary functions
        mock_get_version.return_value = ("2023.12.30", self.mock_api_response["assets"])

        mock_url_response = MagicMock()
        mock_url_response.__enter__.return_value = mock_url_response
        mock_urlopen.return_value = mock_url_response

        progress_callback = MagicMock()

        self.updater.download_yt(progress_callback)

        # Verify that the correct URL was opened
        mock_urlopen.assert_called_once_with("https://fake.url/yt-dlp.exe")

        # Verify that the file was opened for writing
        mock_file.assert_called_once_with(self.updater.yt_dlp_path + ".new", "wb")

        # Verify that shutil.copyfileobj was called
        self.assertTrue(mock_copy.called)

        # Verify that os.replace was called to atomically move the file
        mock_replace.assert_called_once_with(
            self.updater.yt_dlp_path + ".new", self.updater.yt_dlp_path
        )

        # Verify that chmod was called
        self.assertTrue(mock_chmod.called)

        # Verify progress callbacks
        self.assertIn(
            "Downloading yt-dlp 2023.12.30...",
            [call[0][0] for call in progress_callback.call_args_list],
        )
        self.assertIn(
            f"yt-dlp updated to 2023.12.30 at {self.updater.yt_dlp_path}",
            [call[0][0] for call in progress_callback.call_args_list],
        )


if __name__ == "__main__":
    unittest.main()
