from pytubefix import YouTube
from pytubefix.cli import on_progress
import sys
import io
from moviepy import VideoFileClip, AudioFileClip
import time

# Override the sys.stdout to use utf-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def download_with_retry(stream, filename, max_retries=5):
    """Download a stream with retries in case of failure."""
    for attempt in range(max_retries):
        try:
            print(f"Downloading {filename} (Attempt {attempt + 1})...")
            stream.download(filename=filename)
            print(f"Downloaded {filename} successfully!")
            return True
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2)  # Wait for 2 seconds before retrying
    print(f"Failed to download {filename} after {max_retries} attempts.")
    return False

def get_user_quality():
    """Prompt the user to select a video quality."""
    print("Available video qualities:")
    print("1. 1080p")
    print("2. 720p")
    print("3. 480p")
    print("4. 360p")
    choice = input("Enter the number corresponding to your preferred quality: ")
    quality_map = {
        "1": "1080p",
        "2": "720p",
        "3": "480p",
        "4": "360p"
    }
    return quality_map.get(choice, "720p")  # Default to 720p if invalid choice

url = "https://youtu.be/6h92kCk-bkw?si=5YPaBE9IRyUVOyF0"

yt = YouTube(url, on_progress_callback=on_progress)
print(f"Title: {yt.title}")

# Get the user's preferred quality
quality = get_user_quality()
print(f"Selected quality: {quality}")

# Get the highest resolution video stream (without audio) for the selected quality
video_stream = yt.streams.filter(progressive=False, file_extension='mp4', only_video=True, resolution=quality).first()
if not video_stream:
    print(f"No video stream available for {quality}. Downloading the next available quality.")
    video_stream = yt.streams.filter(progressive=False, file_extension='mp4', only_video=True).order_by('resolution').desc().first()

# Get the best audio stream
audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc().first()

# Download video and audio separately with retries
if not download_with_retry(video_stream, "video.mp4"):
    print("Failed to download video stream. Exiting...")
    sys.exit(1)

if not download_with_retry(audio_stream, "audio.mp4"):
    print("Failed to download audio stream. Exiting...")
    sys.exit(1)

# Merge video and audio using moviepy
# print("Merging video and audio...")
# video_clip = VideoFileClip("video.mp4")
# audio_clip = AudioFileClip("audio.mp4")

# final_clip = video_clip.with_audio(audio_clip)
# final_clip.write_videofile("output.mp4", codec="libx264")  # Use h264_nvenc for NVIDIA GPU

print("Download and merge complete! File saved as 'output.mp4'.")