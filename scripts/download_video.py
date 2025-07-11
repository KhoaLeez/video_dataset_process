# scripts/download_video.py
"""
This python scripts handles video downloading in bulk. 
It's only work when called in the anaconda terminal
"""
import yt_dlp
import os

# Set the output directory
OUTPUT_DIR = "D:/Stream_data_process/videos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Example video list — replace with your own links later
video_urls = [
    # format: "https://www.youtube.com/watch?v=YOUR_VIDEO_ID_1",
    "https://www.youtube.com/watch?v=FlqKeW1iWyU",
]

# Download options
ydl_opts = {
    "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
    "merge_output_format": "mp4",
    "outtmpl": os.path.join(OUTPUT_DIR, "%(title)s.%(ext)s"),
    "noplaylist": True,
    "quiet": False,
    "ignoreerrors": True,
}

def download_video(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    for url in video_urls:
        print(f"Downloading: {url}")
        download_video(url)
