from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QDesktopWidget, QComboBox, QProgressBar
)
from PyQt5.QtCore import Qt, QMetaObject, pyqtSignal, QObject, QSize
from pytubefix import YouTube
from moviepy import VideoFileClip, AudioFileClip
import sys, time, threading, os, re
from PyQt5.QtGui import QMovie
from pathlib import Path

class DownloadSignals(QObject):
    update_progress = pyqtSignal(int)
    show_spinner = pyqtSignal(bool)
    update_status = pyqtSignal(str)

class Youtube_Downloader(QWidget):
    def __init__(self):
        super().__init__()
        self.signals = DownloadSignals()
        self.signals.update_progress.connect(self.update_progress_bar)
        self.signals.show_spinner.connect(self.toggle_spinner)
        self.signals.update_status.connect(self.update_status_text)
        
        self.yt_label = QLabel("Paste URL here: ", self)
        self.dropdown_label = QLabel("Select Quality", self)
        self.yt_input = QLineEdit(self)
        self.download_button = QPushButton("Download", self)
        self.combo = QComboBox()
        self.combo.addItems(["360p", "480p", "720p", "1080p"])
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        self.done_label = QLabel("", self)
        self.done_label.setAlignment(Qt.AlignCenter)
        self.spinner_label = QLabel(self)
        
        # Make sure the GIF path is correct
        gif_path = os.path.join(os.path.dirname(__file__), "spinner.gif")
        if not os.path.exists(gif_path):
            print(f"Warning: Spinner GIF not found at {gif_path}")
     
        self.spinner_movie = QMovie(gif_path)
        self.spinner_movie.setScaledSize(QSize(100, 100))  # Set your preferred size
        self.spinner_label.setMovie(self.spinner_movie)
        self.spinner_label.setFixedSize(100, 100)
        self.spinner_label.setAlignment(Qt.AlignCenter)
        self.spinner_label.setVisible(False)
        self.initUI()

    def toggle_spinner(self, show):
        self.spinner_label.setVisible(show)
        if show:
            self.spinner_movie.start()
        else:
            self.spinner_movie.stop()

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

    def update_status_text(self, text):
        self.done_label.setText(text)

    def initUI(self):
        self.setWindowTitle("Youtube Downloader")
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.yt_label)
        vbox.addWidget(self.yt_input)
        vbox.addWidget(self.dropdown_label)
        vbox.addWidget(self.combo)
        vbox.addWidget(self.download_button)
        vbox.addWidget(self.progress_bar)
        vbox.addWidget(self.done_label)
        vbox.addWidget(self.spinner_label)

        self.setLayout(vbox)
        screen = QDesktopWidget().screenGeometry()
        self.resize(800, min(screen.height(), 900))
        self.move((screen.width() - 800) // 2, 0)
        
        self.combo.setObjectName("combo")
        self.yt_input.setObjectName("yt_input")
        self.download_button.setObjectName("download_button")
        self.yt_label.setObjectName("yt_label")
        self.dropdown_label.setObjectName("dropdown_label")
        self.done_label.setObjectName("done_label")
        self.spinner_label.setObjectName("spinner_label")

        self.setStyleSheet("""
            QWidget { 
                background-color: #000000; 
                color: #FFFFFF; 
            }
            QLabel, QPushButton { 
                font-family: calibri; 
            }
            QLabel#yt_label, QLabel#dropdown_label { 
                font-size: 40px; 
                font-style: italic; 
            }
            QLineEdit#yt_input {
                font-size: 40px; background-color: #1e1e1e;
                border: 1px solid #555;
            }
            QPushButton#download_button {
                font-size: 30px; font-weight: bold;
                background-color: #333; border: 2px solid #555;
                border-radius: 8px; padding: 10px;
            }
            QPushButton#download_button:hover { 
                background-color: #555; 
                border-color: #777; 
            }
            QPushButton#download_button:pressed { 
                background-color: #111; 
            }
            QComboBox#combo {
                font-size: 30px; background-color: #1e1e1e;
                color: #FFFFFF; border: 1px solid #555;
            }
            QLabel#done_label{
                font-size: 30px;
                font-style: italic
            }
                        """)



        self.download_button.clicked.connect(self.on_download_clicked)

    def on_download_clicked(self):
        url = self.yt_input.text()
        quality = self.combo.currentText()
        if not url:
            self.done_label.setText("❌ Please enter a URL.")
            return

        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.done_label.setText("")  # Reset label

        thread = threading.Thread(target=self.download_video, args=(url, quality))
        thread.daemon = True  # This ensures the thread won't prevent program exit
        thread.start()

    def download_with_retry(self, stream, filename, max_retries=5):
        for attempt in range(max_retries):
            try:
                print(f"Downloading {filename} (Attempt {attempt + 1})...")
                stream.download(filename=filename)
                print(f"Downloaded {filename} successfully!")
                return True
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(2)
        print(f"Failed to download {filename} after {max_retries} attempts.")
        return False

    def download_video(self, url, quality):
        try:
            self.signals.show_spinner.emit(True)
            self.signals.update_status.emit("🔄 Downloading...")
            
            yt = YouTube(url, on_progress_callback=self.on_progress)
            print(f"Title: {yt.title}")

            # Sanitize the title for use as filename
            safe_title = self.sanitize_filename(yt.title)
            video_filename = f"video_{safe_title}.mp4"
            audio_filename = f"audio_{safe_title}.mp4"
            output_filename = f"{safe_title}.mp4"

            video_stream = yt.streams.filter(progressive=False, file_extension='mp4', only_video=True, resolution=quality).first()
            if not video_stream:
                video_stream = yt.streams.filter(progressive=False, file_extension='mp4', only_video=True).order_by('resolution').desc().first()

            audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc().first()

            if not self.download_with_retry(video_stream, video_filename):
                self.signals.update_status.emit("❌ Video download failed.")
                return
            if not self.download_with_retry(audio_stream, audio_filename):
                self.signals.update_status.emit("❌ Audio download failed.")
                return

            self.signals.update_status.emit("🔄 Merging video and audio...")
            
            video_clip = VideoFileClip(video_filename)
            audio_clip = AudioFileClip(audio_filename)
            video_clip.audio = audio_clip
            final_clip = video_clip
            final_clip.write_videofile(output_filename, codec="libx264")
            
            # Clean up temporary files
            os.remove(video_filename)
            os.remove(audio_filename)
            
            self.signals.show_spinner.emit(False)
            self.signals.update_status.emit(f"✅ Download Complete! Saved as {output_filename}")
            
        except Exception as e:
            print(f"Error: {e}")
            self.signals.update_status.emit(f"❌ Error: {e}")
            self.signals.show_spinner.emit(False)
            
            # Clean up any partial files if error occurred
            for filename in [video_filename, audio_filename, output_filename]:
                if 'filename' in locals() and os.path.exists(filename):
                    try:
                        os.remove(filename)
                    except:
                        pass

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        progress_percent = int((bytes_downloaded / total_size) * 100)
        self.signals.update_progress.emit(progress_percent)
        
        
    def sanitize_filename(self, title):
        """Extract and sanitize the essential part of a YouTube title"""
        # Split on colon, if present
        if ":" in title:
            title = title.split(":")[0]
        # Optional: remove trailing "official", "@artist", or "| Something"
        title = re.split(r"[@|]", title)[0]
        # Remove invalid filename characters
        sanitized = re.sub(r'[\\/*?:"<>|]', "", title)
        # Remove extra whitespace
        return sanitized.strip()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Youtube_Downloader()
    window.show()
    sys.exit(app.exec_())