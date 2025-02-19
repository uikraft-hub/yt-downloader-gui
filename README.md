# SSTube

- ![Active](https://img.shields.io/badge/status-active-47c219.svg)

<p align="center">
    <img src="Favicon.png" width="300" height="300" alt="Icon" />
</p>
  <p>
    SSTube is a powerful, open-source YouTube downloader application that supports multiple download modes—including single videos, playlists, channels (videos and shorts), and even MP3 extractions.
  </p>
  
  <h2>Features</h2>
  <ul>
    <li>
      <strong>Multiple download modes:</strong>
      <ul>
        <li>Single Video / MP3 Only</li>
        <li>Playlist Video / Playlist MP3</li>
        <li>Channel Videos / Channel Videos MP3</li>
        <li>Channel Shorts / Channel Shorts MP3</li>
      </ul>
    </li>
    <li>
      <strong>Integrated ffmpeg updater:</strong> Automatically downloads and installs the latest ffmpeg build.
    </li>
    <li>
      <strong>Activity log:</strong> Displays real-time progress and status messages.
    </li>
    <li>
      <strong>History management:</strong> Options to delete download history.
    </li>
    <li>
      <strong>Bug reporting:</strong> A built-in "Report a Bug" button to help improve the software.
    </li>
  </ul>
  
  <p>
    This project is designed with a clean, modern GUI using Tkinter with ttkthemes and is intended for personal use with potential for further development and contributions from the community.
  </p>
</body>
</html>


  <h1>How to Use SSTube</h1>
  
  <h2>Launching the App</h2>
  <p>Simply run the SSTube executable (or run the script with Python). The main window has three sections:</p>
  <ul>
    <li><strong>Download:</strong> For entering URLs and selecting download modes.</li>
    <li><strong>Activity:</strong> Displays a log of download progress and status messages.</li>
    <li><strong>Settings:</strong> For updating ffmpeg, deleting history, and reporting bugs.</li>
  </ul>

  <h2>Download Modes</h2>
  
  <h3>Single Video / MP3 Only</h3>
  <ul>
    <li><strong>Input:</strong> Paste the URL of a single YouTube video.</li>
    <li><strong>Note:</strong> If the URL looks like a playlist or channel, you will be prompted to select the appropriate mode.</li>
    <li><strong>Quality:</strong> Choose video quality (for video) or audio quality (for MP3).</li>
  </ul>
  
  <h3>Playlist Video / Playlist MP3</h3>
  <ul>
    <li><strong>Input:</strong> Paste the URL of a YouTube playlist.</li>
    <li><strong>Selection:</strong> A new window will list all videos from the playlist. Check the ones you wish to download.</li>
    <li><strong>Quality:</strong> Select video or audio quality accordingly.</li>
  </ul>
  
  <h3>Channel Videos / Channel Videos MP3</h3>
  <ul>
    <li><strong>Input:</strong> Paste the URL of a YouTube channel.</li>
    <li><strong>Note:</strong> If the URL does not include <code>/videos</code>, it will be automatically appended.</li>
    <li><strong>Selection:</strong> A window will list all videos (excluding shorts) for selection.</li>
    <li><strong>Quality:</strong> Choose the desired quality.</li>
  </ul>
  
  <h3>Channel Shorts / Channel Shorts MP3</h3>
  <ul>
    <li><strong>Input:</strong> Paste the URL of a YouTube channel.</li>
    <li><strong>Note:</strong> If the URL does not include <code>/shorts</code>, it will be automatically appended.</li>
    <li><strong>Selection:</strong> A window will list only the shorts for selection.</li>
    <li><strong>Quality:</strong> Choose the desired quality.</li>
  </ul>
  
  <h2>ffmpeg Updater</h2>
  <p>In the Settings panel, click <strong>Update ffmpeg</strong>. A dialog will appear with a progress bar showing the download and extraction progress. This will automatically replace the existing <code>ffmpeg.exe</code> in the <code>bin</code> folder with the latest version.</p>
  
  <h2>Deleting History</h2>
  <p>If you want to clear your download history, click the <strong>Delete History</strong> button in the Settings panel.</p>
  
  <h2>Reporting a Bug</h2>

  <h1>Frequently Asked Questions</h1>
  
  <h2>Q: What is ffmpeg and why is it needed?</h2>
  <p><strong>A:</strong> ffmpeg is a tool used to merge video and audio streams. SSTube uses it to produce a single output file.</p>
  
  <h2>Q: How do I update ffmpeg?</h2>
  <p><strong>A:</strong> Use the <em>Update ffmpeg</em> button in the Settings panel. This downloads the latest build automatically.</p>
  
  <h2>Q: My URL is not working. What should I do?</h2>
  <p><strong>A:</strong> Ensure you are using the correct download mode. For example, use <code>Playlist Video</code> for a playlist URL, or <code>Channel Videos</code> for a channel URL.</p>
  
  <h2>Q: Can I contribute to SSTube?</h2>
  <p><strong>A:</strong> Yes! Please see the Contributing section below for details.</p>
  
  <hr>
  
  <h1>Contributing to SSTube</h1>
  <p>We welcome contributions to SSTube! To get started:</p>
  
  <h3>Fork the Repository</h3>
  <p>Click the <strong>Fork</strong> button on GitHub to create your own copy.</p>
  
  <h3>Clone Your Fork</h3>
  <pre>
git clone https://github.com/UKRProjects/SSTube.git
cd SSTube
  </pre>
  
  <h3>Create a Branch</h3>
  <pre>
git checkout -b feature/YourFeature
  </pre>
  
  <h3>Make Your Changes</h3>
  <p>Follow best practices and ensure your code is well-documented.</p>
  
  <h3>Submit a Pull Request</h3>
  <p>Push your branch and open a pull request. Please include a detailed description of your changes and any related issues.</p>
  
  <h3>Issues</h3>
  <p>Use GitHub Issues to report bugs or suggest features.</p>
  
  <hr>
  
  <h1>License</h1>
  <p>SSTube is released under the <strong>MIT License</strong>. You can view the full license text in the <code>LICENSE</code> file in this repository.</p>
  <p>This license allows you to use, modify, and distribute the software with minimal restrictions.</p>
  
</body>
</html>

  <p>If you encounter an issue, click <strong>Report a Bug</strong> in the Settings panel. This will open your default email client, pre-addressed to the support email (or bug reporting URL), so you can describe the issue.</p>
</body>
</html>


