# scripts/download_video.py
"""
This python scripts handles video downloading in bulk. 
It's only work when called in the anaconda terminal
"""
import yt_dlp
import os
import re
import json
import logging
from time import sleep

# Set the output directory
OUTPUT_DIR = "D:/Stream_data_process/videos" # change this to match your directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set up logging
logging.basicConfig(
    filename='download_log.txt',
    level=logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s'
)

def load_urls(file_path):
    # Load a bunch of URLs from a JSON/text file
    if file_path.endswith('.json'):
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data.get('urls', [])
    else: 
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]

def is_valid_url(url):
    # A siple url validation with regex
    link = r'^https?://(www\)?[\w-]+\\w{2,}/.*$'
    return bool(re.match(link, url))

# Download options
ydl_opts = {
    "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
    "merge_output_format": "mp4",
    "outtmpl": os.path.join(OUTPUT_DIR, "%(title)s.%(ext)s"),
    "noplaylist": True,
    "quiet": False,
    "ignoreerrors": True,
}

def download_video(url, max_retries=3):
    # Download a single video with retrying
    retry_count = 0
    while retry_count < max_retries:
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            logging.info(f"Successfully downloaded: {url}")
            print(f"Success: {url}")
            return
        except Exception as e:
            retry_count += 1
            logging.error("Failed to download {url}: {str(e)}")
            if retry_count == max_retries:
                logging.error(f"Max retries reached for {url}. Skipping.")
                print(f"Failed: {url} after {max_retries} attempts")
                return
            sleep(2**retry_count) # Exponential backoff
                
if __name__ == "__main__":
    video_urls = load_urls('video_urls.json')
    video_urls = [url for url in video_urls if is_valid_url(url)]
    for url in video_urls:
        print(f"Downloading: {url}")
        download_video(url)
