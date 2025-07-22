# scripts/extract_frames.py

import cv2
import os

# Input & output directories
VIDEO_DIR = "D:/Stream_data_process/videos"
FRAME_DIR = "D:/Stream_data_process/frames"
os.makedirs(FRAME_DIR, exist_ok=True)

# Frame extraction settings
FRAME_RATE = 1  # frames per second

def extract_frames_from_video(video_path, output_dir, frame_rate=1):
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    save_path = os.path.join(output_dir, video_name)
    os.makedirs(save_path, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"❌ Failed to open: {video_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    step = int(fps // frame_rate)

    count = 0
    saved = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if count % step == 0:
            frame_file = os.path.join(save_path, f"frame_{saved:05d}.jpg")
            cv2.imwrite(frame_file, frame)
            saved += 1
        count += 1

    cap.release()
    print(f"✅ Extracted {saved} frames from {video_name}")

if __name__ == "__main__":
    for filename in os.listdir(VIDEO_DIR):
        if filename.endswith(".mp4"):
            video_path = os.path.join(VIDEO_DIR, filename)
            extract_frames_from_video(video_path, FRAME_DIR, FRAME_RATE)
