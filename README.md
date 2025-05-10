# 🎬 YouTube Video Downloader

The **YouTube Video Downloader** is a versatile tool that provides both command-line and GUI-based options for downloading YouTube videos. The GUI is designed using **PyQt5**, offering a user-friendly experience.

---

## 🚀 Features

- 🎥 **Video & Audio Downloading**: Downloads video and audio streams separately to ensure optimal quality.
- 🖥️ **Graphical User Interface (GUI)**: A PyQt5-based GUI for easy interaction.
- 🛠️ **Quality Selection**: Users can select their preferred video resolution (e.g., 1080p, 720p, etc.).
- 🔄 **Retry Mechanism**: Retries downloads in case of failures for a seamless experience.
- 🎬 **Automatic Merging**: Combines video and audio streams into a single file using **moviepy**, ensuring a complete video file.

---

## 🧰 Prerequisites

Before running the tool, ensure you have the following installed:

- Python 3
- Required Python libraries:
  - `pytubefix`
  - `moviepy`
  - `PyQt5`

Install the dependencies using pip:

```bash
pip install pytubefix moviepy PyQt5
```

---

## 🛠️ How to Use

### Command-Line Interface (CLI)

1. Clone the repository:

   ```bash
   git clone https://github.com/Rangat001/YT_video_downloder.git
   ```

2. Navigate to the project directory:

   ```bash
   cd YT_video_downloder
   ```

3. Run the script:

   ```bash
   python yt_download_cli.py
   ```

4. Follow the on-screen instructions:
   - Paste the YouTube video URL.
   - Select your preferred video quality from the displayed options.
   - The video and audio will be downloaded and merged automatically.

---

### Graphical User Interface (GUI)

1. Run the GUI script:

   ```bash
   python yt_download_gui.py
   ```

2. Use the PyQt5 GUI to:
   - Paste the YouTube video URL.
   - Select your preferred video quality.
   - Download and manage videos easily.

---

## 📌 Notes

- The tool uses a **retry mechanism** to handle download failures. If a stream fails to download after multiple attempts, the script will exit gracefully.
- The **merging process** is automatic and ensures a complete video file without requiring manual intervention.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve the project.

---

## 💬 Have Questions?

If you have any questions or run into issues, feel free to open an issue in this repository or contact us directly.

---

**Enjoy downloading your favorite YouTube videos!** 🎉
