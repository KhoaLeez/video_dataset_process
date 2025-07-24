import cv2
import os
import csv
import time
import logging
import shutil
from tqdm import tqdm
try:
    from retinaface.pulse_retina import PulseMonitor
except ImportError as e:
    print(f"Error: Could not import PulseMonitor. Ensure retinaface is installed: {e}")
    exit(1)

# Set up logging
logging.basicConfig(
    filename='pulse_analysis_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def check_disk_space(path, min_space_gb=1):
    """Check if there's enough disk space."""
    total, used, free = shutil.disk_usage(path)
    free_gb = free / (1024 ** 3)
    if free_gb < min_space_gb:
        logging.error(f"Insufficient disk space: {free_gb:.2f} GB available, {min_space_gb} GB required")
        print(f"Error: Insufficient disk space ({free_gb:.2f} GB available)")
        return False
    return True

def analyze_video(video_path, output_dir="D:/Stream_data_process/heart_rate_logs", frame_skip=1):
    """Analyze a single video and log heart rate data with metadata."""
    if not check_disk_space(output_dir):
        return

    os.makedirs(output_dir, exist_ok=True)
    pulse_monitor = PulseMonitor()
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        logging.error(f"Could not open video: {video_path}")
        print(f"Error: Could not open video {video_path}")
        return

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps if fps > 0 else 0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    logging.info(f"Processing video: {video_path}, FPS: {fps:.2f}, Duration: {duration:.2f}s, Resolution: {width}x{height}")

    # Prepare CSV output
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    csv_path = os.path.join(output_dir, f"{video_name}_heartrate_log.csv")
    bpms = []
    with open(csv_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Timestamp (s)", "Heart Rate (BPM)"])

        start_time = time.time()
        frame_idx = 0
        pbar = tqdm(total=frame_count, desc=f"Processing {video_name}", unit="frame")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_idx % frame_skip == 0:  # Process every frame_skip-th frame
                try:
                    _, bpm = pulse_monitor.process_frame(frame)
                    timestamp = frame_idx / fps if fps > 0 else time.time() - start_time
                    csv_writer.writerow([f"{timestamp:.2f}", f"{bpm:.1f}"])
                    bpms.append(bpm)
                    print(f"Video: {video_name}, Frame: {frame_idx}, Timestamp: {timestamp:.2f}s, BPM: {bpm:.1f}")
                except Exception as e:
                    logging.error(f"Error processing frame {frame_idx} in {video_path}: {str(e)}")
                    print(f"Error in frame {frame_idx}: {str(e)}")

            frame_idx += 1
            pbar.update(1)

        pbar.close()
        cap.release()

    logging.info(f"Finished processing {video_path}. Output saved to {csv_path}")
    print(f"Finished processing {video_path}")

def batch_analyze_videos(input_dir="D:/Stream_data_process/videos", 
                         output_dir="D:/Stream_data_process/heart_rate_logs", frame_skip=1):
    # Analyze all MP4 videos in the input directory.
    print("Starting batch video analysis...")
    if not check_disk_space(output_dir):
        return

    video_files = [f for f in os.listdir(input_dir) if f.endswith('.mp4')]
    if not video_files:
        logging.warning(f"No MP4 videos found in {input_dir}")
        print(f"No videos found in {input_dir}")
        return

    for video_file in video_files:
        video_path = os.path.join(input_dir, video_file)
        print(f"Analyzing {video_path}...")
        analyze_video(video_path, output_dir, frame_skip)

if __name__ == "__main__":
    batch_analyze_videos(frame_skip=1)  # Adjust frame_skip for faster processing

