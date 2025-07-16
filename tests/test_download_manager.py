import os
import sys
import unittest
from unittest.mock import MagicMock

# Add the 'src' directory to the Python path to allow for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from app.download_manager import DownloadManager

class TestDownloadManager(unittest.TestCase):
    """Tests for the DownloadManager class."""

    def setUp(self):
        """Set up the test environment."""
        # Mock the main application window and its components
        self.mock_main_app = MagicMock()
        self.mock_main_app.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
        
        # Instantiate the DownloadManager with the mocked main app
        self.download_manager = DownloadManager(self.mock_main_app)

    def test_build_video_download_command_best_quality(self):
        """Test building a video download command for the best available quality."""
        yt_dlp_path = os.path.join(self.mock_main_app.base_dir, "bin", "yt-dlp.exe")
        ffmpeg_path = os.path.join(self.mock_main_app.base_dir, "bin", "ffmpeg.exe")
        url = "https://www.youtube.com/watch?v=test"
        save_path = "/fake/path"
        video_quality = "Best Available"

        expected_cmd = [
            yt_dlp_path,
            "--ffmpeg-location", ffmpeg_path,
            "--no-playlist",
            "--output", os.path.join(save_path, "%(title)s.%(ext)s"),
            "--format", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
            "--merge-output-format", "mp4",
            url,
        ]

        cmd = self.download_manager._build_video_download_command(
            yt_dlp_path, ffmpeg_path, url, save_path, video_quality
        )
        self.assertEqual(cmd, expected_cmd)

    def test_build_video_download_command_specific_quality(self):
        """Test building a video download command for a specific quality (e.g., 1080p)."""
        yt_dlp_path = os.path.join(self.mock_main_app.base_dir, "bin", "yt-dlp.exe")
        ffmpeg_path = os.path.join(self.mock_main_app.base_dir, "bin", "ffmpeg.exe")
        url = "https://www.youtube.com/watch?v=test"
        save_path = "/fake/path"
        video_quality = "1080p"

        expected_cmd = [
            yt_dlp_path,
            "--ffmpeg-location", ffmpeg_path,
            "--no-playlist",
            "--output", os.path.join(save_path, "%(title)s.%(ext)s"),
            "--format", "bestvideo[height<=1080]+bestaudio/merge",
            "--merge-output-format", "mp4",
            url,
        ]

        cmd = self.download_manager._build_video_download_command(
            yt_dlp_path, ffmpeg_path, url, save_path, video_quality
        )
        self.assertEqual(cmd, expected_cmd)

    def test_build_audio_download_command(self):
        """Test building an audio download command."""
        yt_dlp_path = os.path.join(self.mock_main_app.base_dir, "bin", "yt-dlp.exe")
        ffmpeg_path = os.path.join(self.mock_main_app.base_dir, "bin", "ffmpeg.exe")
        url = "https://www.youtube.com/watch?v=test"
        save_path = "/fake/path"
        audio_quality = "192"

        expected_cmd = [
            yt_dlp_path,
            "--ffmpeg-location", ffmpeg_path,
            "--no-playlist",
            "--output", os.path.join(save_path, "%(title)s.%(ext)s"),
            "--format", "bestaudio/best",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", audio_quality,
            url,
        ]

        cmd = self.download_manager._build_audio_download_command(
            yt_dlp_path, ffmpeg_path, url, save_path, audio_quality
        )
        self.assertEqual(cmd, expected_cmd)

if __name__ == '__main__':
    unittest.main()
