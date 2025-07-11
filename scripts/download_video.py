"""
This file handles the download of videos from streams.
The tool used here is 
"""

# scripts/download_video.py

import yt_dlp
import os

# Set the output directory
OUTPUT_DIR = "../videos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Example video list — replace with your own links later
video_urls = [
    # format: "https://www.youtube.com/watch?v=YOUR_VIDEO_ID_1",
    "https://www.youtube.com/watch?v=0Hv7q6vdrVs",
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
