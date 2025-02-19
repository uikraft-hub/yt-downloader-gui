import os
import threading
import time
import json
import webbrowser
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import yt_dlp
from ttkthemes import ThemedStyle
from PIL import Image, ImageTk
import urllib.request
import zipfile
import tempfile
import shutil


class SSTubeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SSTube")
        self.root.geometry("1100x750")
        self.root.config(bg="white")
        # Set window icon from Favicon.png
        try:
            icon_img = ImageTk.PhotoImage(Image.open("Favicon.png"))
            self.root.iconphoto(False, icon_img)
        except Exception as e:
            print("Error setting window icon:", e)

        self.style = ThemedStyle(self.root)
        self.style.set_theme("arc")

        # Download queue and history
        self.download_queue = []  # Each task is a dict
        self.history = []
        self.download_thread = None
        self.downloading = False  # Sequential download flag

        # Modes: Single Video, MP3 Only, Playlist Video, Playlist MP3,
        # Channel Videos, Channel Videos MP3, Channel Shorts, Channel
        # Shorts MP3
        self.mode_var = tk.StringVar(value="Single Video")
        self.audio_quality_var = tk.StringVar(value="320")
        self.video_quality_var = tk.StringVar(value="Best Available")

        self.icons = {
            "download": self.load_icon("assets/download.png"),
            "activity": self.load_icon("assets/activity.png"),
            "settings": self.load_icon("assets/settings.png"),
        }

        try:
            light_img = Image.open(
                "assets/light.png").resize((100, 100), Image.LANCZOS)
            dark_img = Image.open(
                "assets/dark.png").resize((100, 100), Image.LANCZOS)
            self.light_img = ImageTk.PhotoImage(light_img)
            self.dark_img = ImageTk.PhotoImage(dark_img)
        except Exception as e:
            print("Error loading theme images:", e)
            self.light_img = None
            self.dark_img = None

        self.load_history()
        self.create_menubar()
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        self.create_sidebar()
        self.frames = {
            "Download": self.create_download_frame(),
            "Activity": self.create_activity_frame(),
            "Settings": self.create_settings_frame(),
        }
        self.status_bar = ttk.Label(
            self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.show_frame("Download")

    def load_icon(self, path):
        try:
            img = Image.open(path)
            return ImageTk.PhotoImage(img.resize((32, 32), Image.LANCZOS))
        except Exception as e:
            print(f"Error loading icon {path}: {e}")
            return None

    def create_menubar(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

    def show_about(self):
        messagebox.showinfo(
            "About SSTube",
            "SSTube Video Downloader\nVersion 1.0\nDeveloped by Your Name\n\n"
            "Report bugs via the 'Report a Bug' option in Settings.",
        )

    def update_status(self, message):
        if hasattr(self, "status_bar"):
            self.status_bar.config(text=message)

    def log_message(self, msg):
        if hasattr(self, "log_text"):
            self.log_text.insert(tk.END, msg + "\n")
            self.log_text.see(tk.END)
        print(msg)

    def create_sidebar(self):
        sidebar = ttk.Frame(self.main_container, width=150, relief=tk.RIDGE)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        header = ttk.Label(
            sidebar, text="SSTube", font=(
                "Helvetica", 16, "bold"))
        header.pack(pady=20)
        options = ["Download", "Activity", "Settings"]
        self.sidebar_buttons = {}
        for option in options:
            icon = self.icons.get(option.lower())
            btn = ttk.Button(
                sidebar,
                text=option,
                image=icon,
                compound=tk.TOP,
                command=lambda o=option: self.show_frame(o),
            )
            btn.pack(pady=10, fill=tk.X, padx=10)
            self.sidebar_buttons[option] = btn

    def show_frame(self, name):
        if hasattr(self, "current_frame") and self.current_frame:
            self.current_frame.pack_forget()
        self.current_frame = self.frames[name]
        self.current_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        for btn in self.sidebar_buttons.values():
            btn.state(["!pressed"])
        self.sidebar_buttons[name].state(["pressed"])
        self.update_status(f"{name} section active")

    def create_download_frame(self):
        frame = ttk.Frame(self.main_container, padding=20)
        url_label = ttk.Label(
            frame,
            text="Enter YouTube URL (or Playlist/Channel URL):",
            font=("Helvetica", 12),
        )
        url_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        self.url_entry = ttk.Entry(frame, width=70, font=("Helvetica", 11))
        self.url_entry.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)
        path_label = ttk.Label(
            frame, text="Save Location:", font=(
                "Helvetica", 12))
        path_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        self.save_path = tk.StringVar()
        path_entry = ttk.Entry(
            frame,
            textvariable=self.save_path,
            state="readonly",
            width=50,
            font=("Helvetica", 11),
        )
        path_entry.grid(row=3, column=0, sticky=tk.W, pady=5)
        browse_btn = ttk.Button(
            frame, text="Browse Folder", command=self.select_save_path
        )
        browse_btn.grid(row=3, column=1, sticky=tk.W, padx=10, pady=5)
        mode_label = ttk.Label(
            frame, text="Download Mode:", font=(
                "Helvetica", 12))
        mode_label.grid(row=4, column=0, sticky=tk.W, pady=5)
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
        self.mode_menu = ttk.Combobox(
            frame,
            textvariable=self.mode_var,
            values=modes,
            state="readonly",
            font=("Helvetica", 11),
        )
        self.mode_menu.grid(row=5, column=0, sticky=tk.W, pady=5)
        self.mode_menu.bind("<<ComboboxSelected>>", self.mode_changed)
        self.audio_quality_label = ttk.Label(
            frame, text="Audio Quality (kbps):", font=("Helvetica", 12)
        )
        self.audio_quality_menu = ttk.Combobox(
            frame,
            textvariable=self.audio_quality_var,
            values=["320", "192", "128"],
            state="readonly",
            font=("Helvetica", 11),
        )
        self.video_quality_label = ttk.Label(
            frame, text="Video Quality:", font=("Helvetica", 12)
        )
        self.video_quality_menu = ttk.Combobox(
            frame,
            textvariable=self.video_quality_var,
            values=[
                "Best Available",
                "4320p 8K",
                "2160p 4K",
                "1440p 2K",
                "1080p Full HD",
                "720p HD",
                "480p Standard",
                "360p Medium",
            ],
            state="readonly",
            font=("Helvetica", 11),
        )
        self.video_quality_label.grid(row=6, column=0, sticky=tk.W, pady=5)
        self.video_quality_menu.grid(row=7, column=0, sticky=tk.W, pady=5)
        self.audio_quality_label.grid_forget()
        self.audio_quality_menu.grid_forget()
        add_btn = ttk.Button(
            frame,
            text="Add to Queue",
            command=self.add_to_queue)
        add_btn.grid(row=8, column=0, columnspan=2, pady=20)
        return frame

    def mode_changed(self, event=None):
        mode = self.mode_var.get()
        if "MP3" in mode:
            self.audio_quality_label.grid(row=6, column=0, sticky=tk.W, pady=5)
            self.audio_quality_menu.grid(row=7, column=0, sticky=tk.W, pady=5)
            self.video_quality_label.grid_forget()
            self.video_quality_menu.grid_forget()
        else:
            self.video_quality_label.grid(row=6, column=0, sticky=tk.W, pady=5)
            self.video_quality_menu.grid(row=7, column=0, sticky=tk.W, pady=5)
            self.audio_quality_label.grid_forget()
            self.audio_quality_menu.grid_forget()

    def select_save_path(self):
        path = filedialog.askdirectory()
        if path:
            self.save_path.set(path)
            self.update_status("Save path selected")

    def add_to_queue(self):
        url = self.url_entry.get().strip()
        save_path = self.save_path.get().strip()
        mode = self.mode_var.get()
        if not url or not save_path:
            messagebox.showerror(
                "Error", "Please enter a URL and select a save path.")
            return
        if mode in ["Single Video", "MP3 Only"]:
            if "list=" in url or "youtube.com/@" in url or "/channel/" in url:
                messagebox.showerror(
                    "Error", "The URL appears to be a playlist or channel. Please select "
                    "the appropriate mode.", )
                return
        elif mode in ["Playlist Video", "Playlist MP3"]:
            if "list=" not in url:
                messagebox.showerror(
                    "Error", "The URL does not appear to be a playlist. Please select the "
                    "appropriate mode.", )
                return
        elif mode in [
            "Channel Videos",
            "Channel Videos MP3",
            "Channel Shorts",
            "Channel Shorts MP3",
        ]:
            if ("youtube.com/@" not in url) and ("/channel/" not in url):
                messagebox.showerror(
                    "Error", "The URL does not appear to be a channel. Please select the "
                    "appropriate mode.", )
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
                "audio_quality": (
                    self.audio_quality_var.get() if "MP3" in mode else None
                ),
                "video_quality": (
                    self.video_quality_var.get()
                    if mode == "Single Video"
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
                messagebox.showerror("Error", "No playlist entries found.")
                return
            entries = playlist_info["entries"]
        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to extract playlist info: {e}")
            return

        sel_win = tk.Toplevel(self.root)
        sel_win.title("Select Videos from Playlist")
        sel_win.geometry("600x400")
        sel_frame = ttk.Frame(sel_win, padding=10)
        sel_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(sel_frame)
        scrollbar = ttk.Scrollbar(
            sel_frame,
            orient="vertical",
            command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.playlist_vars = []
        for entry in entries:
            if not entry:
                continue
            video_url = entry.get("url")
            if video_url and not video_url.startswith("http"):
                video_url = playlist_info.get("webpage_url", "") + video_url
            title = entry.get("title", "Unknown Title")
            var = tk.BooleanVar(value=True)
            chk = ttk.Checkbutton(scrollable_frame, text=title, variable=var)
            chk.pack(anchor="w", pady=2)
            self.playlist_vars.append((video_url, title, var))

        def download_selected():
            count = 0
            for video_url, title, var in self.playlist_vars:
                if var.get():
                    task = {
                        "url": video_url,
                        "save_path": save_path,
                        "mode": mode,
                        "audio_quality": (
                            self.audio_quality_var.get() if "MP3" in mode else None
                        ),
                        "video_quality": (
                            self.video_quality_var.get()
                            if mode == "Playlist Video"
                            else "Best Available"
                        ),
                    }
                    self.download_queue.append(task)
                    count += 1
            if count == 0:
                messagebox.showinfo("Info", "No videos selected.")
            else:
                self.log_message(
                    f"{count} videos added to queue from playlist.")
                self.process_queue()
            sel_win.destroy()

        download_btn = ttk.Button(
            sel_win, text="Download Selected", command=download_selected
        )
        download_btn.pack(pady=10)

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
                messagebox.showerror("Error", "No videos found for channel.")
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
            messagebox.showerror(
                "Error", f"Failed to extract channel info: {e}")
            return

        sel_win = tk.Toplevel(self.root)
        sel_win.title("Select Videos from Channel")
        sel_win.geometry("600x400")
        sel_frame = ttk.Frame(sel_win, padding=10)
        sel_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(sel_frame)
        scrollbar = ttk.Scrollbar(
            sel_frame,
            orient="vertical",
            command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.channel_vars = []
        for entry in filtered:
            video_url = entry.get("url")
            if video_url and not video_url.startswith("http"):
                video_url = channel_info.get("webpage_url", "") + video_url
            title = entry.get("title", "Unknown Title")
            var = tk.BooleanVar(value=True)
            chk = ttk.Checkbutton(scrollable_frame, text=title, variable=var)
            chk.pack(anchor="w", pady=2)
            self.channel_vars.append((video_url, title, var))

        def download_selected():
            count = 0
            for video_url, title, var in self.channel_vars:
                if var.get():
                    task = {
                        "url": video_url,
                        "save_path": save_path,
                        "mode": mode,
                        "audio_quality": (
                            self.audio_quality_var.get() if "MP3" in mode else None
                        ),
                        "video_quality": (
                            self.video_quality_var.get()
                            if mode in ["Channel Videos", "Channel Shorts"]
                            else "Best Available"
                        ),
                    }
                    self.download_queue.append(task)
                    count += 1
            if count == 0:
                messagebox.showinfo("Info", "No videos selected.")
            else:
                self.log_message(
                    f"{count} videos added to queue from channel.")
                self.process_queue()
            sel_win.destroy()

        download_btn = ttk.Button(
            sel_win, text="Download Selected", command=download_selected
        )
        download_btn.pack(pady=10)

    def create_activity_frame(self):
        frame = ttk.Frame(self.main_container, padding=20)
        self.log_text = scrolledtext.ScrolledText(
            frame, state="normal", font=("Helvetica", 10)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        return frame

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
                "outtmpl": os.path.join(
                    save_path,
                    "%(title)s.%(ext)s"),
                "ffmpeg_location": os.path.join(
                    os.getcwd(),
                    "bin",
                    "ffmpeg.exe"),
                "noplaylist": True,
                "progress_hooks": [
                    self.update_progress],
                "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
                "merge_output_format": "mp4",
            }
            if video_quality != "Best Available":
                height = video_quality.split("p")[0]
                ydl_opts["format"] = (
                    f"bestvideo[ext=mp4][height<={height}]+"
                    "bestaudio[ext=m4a]/mp4")
        elif mode in [
            "MP3 Only",
            "Playlist MP3",
            "Channel Videos MP3",
            "Channel Shorts MP3",
        ]:
            ydl_opts = {
                "outtmpl": os.path.join(
                    save_path,
                    "%(title)s.%(ext)s"),
                "ffmpeg_location": os.path.join(
                    os.getcwd(),
                    "bin",
                    "ffmpeg.exe"),
                "noplaylist": True,
                "progress_hooks": [
                    self.update_progress],
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": task["audio_quality"],
                    }],
            }
        else:
            messagebox.showerror("Error", "Invalid download mode.")
            self.downloading = False
            return

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get("title", "Unknown")
                self.log_message(f"Downloading: {title}")
                ydl.download([url])
                self.log_message(f"Download completed: {title}")
                self.history.append(
                    {
                        "title": title,
                        "url": url,
                        "mode": mode,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    }
                )
                self.save_history()
        except Exception as e:
            messagebox.showerror("Error", f"Download failed: {e}")
            self.log_message("Download failed")
        finally:
            self.downloading = False
            self.process_queue()

    def update_progress(self, d):
        if d["status"] == "downloading":
            percent_str = d.get("_percent_str", "0%").strip()
            speed = d.get("_speed_str", "0 KB/s").strip()
            self.log_message(
                f"{d['info_dict'].get('title','Unknown')} - "
                f"{percent_str} at {speed}"
            )
        elif d["status"] == "finished":
            self.log_message(
                f"{d['info_dict'].get('title','Unknown')} - Download finished."
            )

    def create_settings_frame(self):
        frame = ttk.Frame(self.main_container, padding=20)
        report_btn = ttk.Button(
            frame,
            text="Report a Bug",
            command=self.open_email)
        report_btn.pack(pady=5)
        update_ffmpeg_btn = ttk.Button(
            frame, text="Update ffmpeg", command=self.update_ffmpeg
        )
        update_ffmpeg_btn.pack(pady=10)
        delete_history_btn = ttk.Button(
            frame, text="Delete History", command=self.delete_history
        )
        delete_history_btn.pack(pady=10)
        history_label = ttk.Label(
            frame, text="Download History:", font=("Helvetica", 12)
        )
        history_label.pack(pady=10, anchor=tk.W)
        self.history_text = scrolledtext.ScrolledText(
            frame, height=10, state="disabled", font=("Helvetica", 10)
        )
        self.history_text.pack(fill=tk.BOTH, expand=True)
        self.update_history_display()
        disclaimer = (
            "SSTube Video Downloader is intended for personal use only. "
            "We do not encourage any malicious behavior and cannot be held "
            "responsible for any misuse."
        )
        disclaimer_label = ttk.Label(
            frame, text=disclaimer, wraplength=500, font=(
                "Helvetica", 9, "italic"))
        disclaimer_label.pack(pady=20, anchor=tk.W)
        contact_btn = ttk.Button(
            frame,
            text="Contact Us",
            command=self.open_email)
        contact_btn.pack(pady=10)
        return frame

    def update_ffmpeg(self):
        confirm = messagebox.askyesno(
            "Update ffmpeg",
            "This will download the latest ffmpeg build and replace the current "
            "executable. Continue?",
        )
        if not confirm:
            return

        progress_win = tk.Toplevel(self.root)
        progress_win.title("Updating ffmpeg")
        progress_win.geometry("400x150")
        progress_label = ttk.Label(
            progress_win, text="Downloading ffmpeg update...")
        progress_label.pack(padx=10, pady=10)
        progress_bar = ttk.Progressbar(
            progress_win, orient="horizontal", mode="determinate", length=300
        )
        progress_bar.pack(padx=10, pady=10)
        self.root.update()

        def reporthook(block_num, block_size, total_size):
            downloaded = block_num * block_size
            if total_size > 0:
                percent = int(downloaded * 100 / total_size)
                progress_bar["value"] = percent
                progress_win.update_idletasks()

        try:
            update_url = (
                "https://www.gyan.dev/ffmpeg/builds/"
                "ffmpeg-release-essentials.zip")
            temp_zip_path, _ = urllib.request.urlretrieve(
                update_url, reporthook=reporthook
            )
            progress_label.config(text="Download complete. Extracting...")
            self.log_message("Downloaded ffmpeg archive.")
            with zipfile.ZipFile(temp_zip_path, "r") as zip_ref:
                target_file = None
                for file in zip_ref.namelist():
                    if file.lower().endswith("ffmpeg.exe"):
                        target_file = file
                        break
                if not target_file:
                    raise Exception("ffmpeg.exe not found in the archive.")
                temp_extract_dir = tempfile.mkdtemp()
                zip_ref.extract(target_file, temp_extract_dir)
                extracted_path = os.path.join(temp_extract_dir, target_file)
                target_path = os.path.join(os.getcwd(), "bin", "ffmpeg.exe")
                shutil.copy(extracted_path, target_path)
                self.log_message("ffmpeg has been updated successfully.")
                messagebox.showinfo(
                    "Update Complete", "ffmpeg has been updated successfully."
                )
                shutil.rmtree(temp_extract_dir)
        except Exception as e:
            messagebox.showerror("Update Failed", f"ffmpeg update failed: {e}")
            self.log_message(f"ffmpeg update failed: {e}")
        finally:
            progress_win.destroy()

    def delete_history(self):
        confirm = messagebox.askyesno(
            "Delete History",
            "Are you sure you want to delete the download history?")
        if confirm:
            self.history = []
            if os.path.exists("history.json"):
                os.remove("history.json")
            self.update_history_display()
            self.log_message("Download history deleted.")

    def open_email(self):
        webbrowser.open("mailto:ukrpurojekuto@gmail.com")

    def load_history(self):
        if os.path.exists("history.json"):
            try:
                with open("history.json", "r") as f:
                    self.history = json.load(f)
            except Exception as e:
                print("Error loading history:", e)
                self.history = []

    def save_history(self):
        try:
            with open("history.json", "w") as f:
                json.dump(self.history, f, indent=4)
        except Exception as e:
            print("Error saving history:", e)

    def update_history_display(self):
        if hasattr(self, "history_text"):
            self.history_text.config(state="normal")
            self.history_text.delete(1.0, tk.END)
            for entry in self.history[-10:]:
                self.history_text.insert(
                    tk.END,
                    f"{entry['timestamp']} - {entry['title']} "
                    f"({entry.get('mode', 'N/A')})\n",
                )
            self.history_text.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = SSTubeGUI(root)
    root.mainloop()
