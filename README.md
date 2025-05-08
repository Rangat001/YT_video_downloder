# YouTube Video Downloader

The **YouTube Video Downloader** is a command-line tool that allows you to download YouTube videos easily. It supports downloading video and audio streams separately, with an optional merging feature for combining both into a single file.

---

## 🚀 Features

- 🎥 **Video & Audio Downloading**: Downloads video and audio streams separately to ensure optimal quality.
- 🛠️ **Quality Selection**: Users can select their preferred video resolution (e.g., 1080p, 720p, etc.).
- 🔄 **Retry Mechanism**: Retries downloads in case of failures for a seamless experience.
- 🎬 **Optional Merging**: Combines video and audio streams into a single file using `moviepy` (disabled by default to save processing power).

---

## 🧰 Prerequisites

Before running the tool, ensure you have the following installed:

- **Python 3.x**
- Required Python libraries:
  - `pytubefix`
  - `moviepy`

Install the dependencies using pip:

```bash
pip install pytubefix moviepy
```

## 🛠️ How to Use
Follow these simple steps to get started:

1.Clone the repository:

```bash
git clone https://github.com/Rangat001/YT_video_downloder.git
```

2.Navigate to the project directory:

```bash
cd YT_video_downloder
```

3.Run the script:

```bash
python yt_download_cli.py
```

4.Follow the on-screen instructions:

-Paste the YouTube video URL.

-Select your preferred video quality from the displayed options.

-The video and audio will be downloaded separately.


## 🔧 Enabling Merging (Optional)

By default, the merging functionality is disabled to save processing power. If you wish to enable it:


1.Open the yt_download_cli.py file in a text editor.


2.Uncomment the following lines (69-74):

```Python
print("Merging video and audio...")
video_clip = VideoFileClip("video.mp4")
audio_clip = AudioFileClip("audio.mp4")
final_clip = video_clip.with_audio(audio_clip)
final_clip.write_videofile("output.mp4", codec="libx264")
Save the file and rerun the script. The output file will be saved as output.mp4.
```


## 📌 Notes

The tool uses a retry mechanism to handle download failures. If a stream fails to download after multiple attempts, the script will exit gracefully.
The merging process requires additional processing power and may take some time for large files.





## 🤝 Contributing
Contributions are welcome! Feel free to open issues or submit pull requests to improve the project.


## 💬 Have Questions?
If you have any questions or run into issues, feel free to open an issue in this repository or contact us directly.

Enjoy downloading your favorite YouTube videos! 🎉


---


### How to Add This to Your Repository

1. Navigate to the [Create New File](https://github.com/Rangat001/YT_video_downloder/new/main?filename=README.md) page in your repository.
2. Copy and paste the above content into the file editor.
3. Commit the new file to your repository.

Let me know if you need further assistance! 🚀
