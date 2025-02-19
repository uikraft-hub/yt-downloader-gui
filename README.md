# SSTube

<p align="center">
    <img src="Favicon.png" width="300" height="300" alt="Icon" />
</p>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
#SSTube - YouTube Downloader#
    
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 20px;
      line-height: 1.6;
      color: #333;
    }
    h1, h2, h3 {
      color: #2C3E50;
    }
    ul {
      margin-left: 20px;
    }
    li {
      margin-bottom: 5px;
    }
    strong {
      color: #000;
    }
  </style>
</head>
<body>
  <h1>SSTube</h1>
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


<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
# How to Use SSTube
    
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 20px;
      line-height: 1.6;
      color: #333;
    }
    h1, h2, h3 {
      color: #222;
    }
    code {
      background-color: #f4f4f4;
      padding: 2px 4px;
      border-radius: 4px;
    }
    ul {
      margin-left: 20px;
    }
    li {
      margin-bottom: 5px;
    }
  </style>
</head>
<body>
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
  <p>If you encounter an issue, click <strong>Report a Bug</strong> in the Settings panel. This will open your default email client, pre-addressed to the support email (or bug reporting URL), so you can describe the issue.</p>
</body>
</html>


