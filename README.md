# Eye-Tracker
 
A real-time face-tracking pan-tilt camera mount built with Python, OpenCV, and Arduino. The system detects a face via webcam, computes its offset from the frame's center, and smooths that signal before converting it into servo commands, driving a two-axis (pan/tilt) hardware rig that physically follows the detected face.
 
This is an active hobby/learning project. The core software to hardware pipeline is fully working; physical mounting and additional features are in progress.
 
## How it works
 
1. **Capture** — a webcam feed is read frame-by-frame using OpenCV.
2. **Detect** — each frame is converted to grayscale and passed through a Haar cascade classifier (`haarcascade_frontalface_default.xml`) to detect faces.
3. **Select** — if multiple faces (or false positives) are detected, the largest bounding box is selected as the tracking target.
4. **Offset** — the face's center is compared against the frame's center to compute an (x, y) offset.
5. **Smooth** — an exponential moving average (EMA) is applied to the offset to reduce frame-to-frame jitter.
6. **Map** — the smoothed offset is linearly mapped from pixel space into a 0–180° servo angle range for each axis.
7. **Transmit** — both angles are packed into a single comma-delimited message and sent over serial (USB) to an Arduino.
8. **Actuate** — the Arduino parses the incoming message and drives two servos (pan and tilt) to physically point toward the detected face.
## Tech stack
 
- **Python** — OpenCV (`opencv-contrib-python`), `pyserial`
- **C++ (Arduino)** — Arduino `Servo` library, custom serial parsing
- **Hardware** — Arduino Uno R3, 2× MG90S metal-gear micro servos
## Features
 
- Real-time face detection and tracking from a live webcam feed
- Largest-face selection to reduce false-positive interference
- EMA-based signal smoothing for stable, non-jittery servo motion
- Custom two-value serial protocol for synchronized pan/tilt control
- Two-axis (pan + tilt) physical tracking via stacked servos
## Known limitations
 
- Detection is based on Haar cascades, which are sensitive to lighting and generally only detect frontal (non-rotated) faces. A more robust detector (e.g. MediaPipe) is being explored as a future upgrade.
- Under sustained rapid movement, serial communication can occasionally lag due to buffer backlog; a more robust buffering/throttling strategy is still being refined.
- Physical camera/phone mounting is still in progress, current hardware proves out the tracking pipeline on bare servos.
## Planned features
 
- More robust, lighting/angle-resilient face detection
- Specific-person face recognition
- Hand gesture recognition
- Physical camera/phone mount
- Local trigger integration with other personal projects
## Setup
 
### Software
1. Clone this repository.
2. Create and activate a virtual environment:
```
   python -m venv .venv
   .venv\Scripts\Activate.ps1
```
3. Install dependencies:
```
   pip install opencv-contrib-python pyserial
```
4. Update the `COM` port in `tracker.py` to match your Arduino's port.
### Hardware
1. Wire the pan servo's signal pin to Arduino pin 9, and the tilt servo's signal pin to Arduino pin 10.
2. Connect both servos' power and ground to the Arduino's 5V and GND pins.
3. Upload the Arduino sketch to your board via the Arduino IDE.
4. Connect the Arduino to your computer via USB and run:
```
   python tracker.py
```
 
## Author
Andrew Gould — [GitHub](https://github.com/AGould1)
 
