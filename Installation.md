<h1>SSTube Installation Guide</h1>

  <h2>Requirements</h2>
  <ul>
    <li><strong>Python 3.7+</strong> (recommended version: 3.8 or higher)</li>
    <li><strong>yt_dlp</strong>
      <pre><code>pip install -U yt-dlp</code></pre>
    </li>
    <li><strong>ttkthemes</strong>
      <pre><code>pip install ttkthemes</code></pre>
    </li>
    <li><strong>Pillow</strong>
      <pre><code>pip install Pillow</code></pre>
    </li>
    <li><strong>tqdm</strong>
      <pre><code>pip install tqdm</code></pre>
    </li>
    <li><strong>FFmpeg</strong>  
      <p>The application requires <code>ffmpeg.exe</code> to merge video and audio streams.</p>
      <p class="note">Note: SSTube includes a bundled updater to download and update ffmpeg automatically.</p>
    </li>
  </ul>

  <h2>Running as a Script</h2>
  <ol>
    <li>Clone the repository:
      <pre><code>git clone https://github.com/UKRProjects/SSTube.git
cd SSTube</code></pre>
    </li>
    <li>Ensure all assets are in place:
      <ul>
        <li><code>bin/ffmpeg.exe</code> (or use the updater from the Settings panel)</li>
        <li><code>assets/</code> folder (containing icons and theme images)</li>
      </ul>
    </li>
    <li>Run the script:
      <pre><code>python sstube.py</code></pre>
    </li>
  </ol>

  <h2>Creating a Standalone Windows App</h2>
  <p>To compile SSTube into a standalone executable with an installer, you can use PyInstaller and Inno Setup (or NSIS).</p>

  <h3>Using PyInstaller</h3>
  <ol>
    <li>Install PyInstaller:
      <pre><code>pip install pyinstaller</code></pre>
    </li>
    <li>Run PyInstaller:
      <pre><code>pyinstaller --onefile --windowed sstube.py</code></pre>
      <p>This creates a standalone executable in the <code>dist</code> folder.</p>
    </li>
  </ol>

  <h3>Creating an Installer with Inno Setup</h3>
  <ol>
    <li>Download and install <a href="http://www.jrsoftware.org/isinfo.php" target="_blank">Inno Setup</a>.</li>
    <li>Create a new Inno Setup script that:
      <ul>
        <li>Specifies the target install directory.</li>
        <li>Copies the executable, the <code>bin</code> folder with <code>ffmpeg.exe</code>, and the <code>assets</code> folder.</li>
        <li>Creates desktop and start menu shortcuts.</li>
      </ul>
    </li>
    <li>Compile the Inno Setup script to generate an installer EXE.</li>
  </ol>

  <h2>Additional Information</h2>
  <p>For detailed documentation, bug reporting, and contribution guidelines, please refer to the project Wiki on GitHub.</p>

</body>
</html>
