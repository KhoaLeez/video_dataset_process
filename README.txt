# Streamer Video Dataset Processing

This repository contains tools and scripts for processing gameplay videos of streamers, with the aim of analyzing facial expressions, gaze, and physiological signals like pupil dilation. The project supports automatic frame extraction, facial region cropping, and facial feature tracking for large batches of video data.

The goal is to explore how visible biometric cues — such as facial emotion or gaze direction — relate to gameplay events, potentially uncovering patterns in user experience or stress during gaming.

This is part of an ongoing Bachelor thesis project involving:
- **Computer Vision**
- **Gamification and player affect**
- **Non-invasive biometric signal processing**
- **Scalable streamer data analysis**

## Features
- Batch video downloader (YouTube etc.)
- Frame extractor with `ffmpeg` (planned)
- Face detection & landmark extraction (planned)
- Pupil/eye/gaze analysis pipeline (planned)
- Emotion detection from facial features (planned)

## Requirements
To be listed in `environment.yml` (conda). Will include:
- `opencv-python`
- `mediapipe`
- `ffmpeg-python`
- `pandas`, `numpy`
- `yt-dlp` (for video fetching)

## Status
🚧 This project is a work in progress and intended for research prototyping.

## License:

- To be updated