# Driver Drowsiness Detection System

A real-time Driver Drowsiness Detection System built using OpenCV that monitors a driver's eyes through a webcam and triggers an audible alarm if prolonged eye closure is detected.

The project uses Haar Cascade face and eye detection along with a temporal state management algorithm to reduce false alarms. It also displays real-time monitoring information including detection status, alert count, timestamp, and approximate location.

---

## Features

- Real-time face detection
- Eye detection using Haar Cascades
- Drowsiness detection based on prolonged eye closure
- False alarm reduction using temporal confirmation logic
- Multithreaded alarm system
- Live status dashboard
- Real-time alert counter
- Approximate location display (GPS / Google API / IP fallback)
- Modular project architecture


---

## Project Structure

```
Driver-Drowsiness-Detection/
│
├── app.py
├── config.py
├── location_service.py
├── requirements.txt
│
├── detection/
│   ├── face_eye_detector.py
│   └── state_manager.py
│
├── alarm.py
│
├── assets/
│   ├── demo.gif
│   └── screenshot.png
│
└── README.md
```

---

## How it Works

```
Webcam
    │
    ▼
Capture Frame
    │
    ▼
Face Detection
(Haar Cascade)
    │
    ▼
Eye Detection
(Haar Cascade)
    │
    ▼
Eye State Analysis
(Open / Closed)
    │
    ▼
Temporal State Manager
    │
    ▼
Eye Closed > Threshold
    │
    ▼
Alarm Thread
```

---

## Detection Pipeline

1. Capture webcam frames.
2. Detect the largest face.
3. Detect both eyes within the upper face region.
4. Track consecutive open/closed frames.
5. Measure continuous eye closure duration.
6. Trigger alarm when eye closure exceeds threshold.
7. Display status on live dashboard.

---

## Technologies Used

- Python
- OpenCV
- NumPy
- Multithreading
- Haar Cascade Classifiers

---

## Installation

Clone the repository

```bash
git clone https://github.com/yourusername/Driver-Drowsiness-Detection.git
```

Move into the project

```bash
cd Driver-Drowsiness-Detection
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run

```bash
python app.py
```

---

## Configuration

The following parameters can be changed in `config.py`.

| Parameter | Description |
|-----------|-------------|
| CAMERA_INDEX | Camera index |
| FRAME_WIDTH | Camera resolution |
| FRAME_HEIGHT | Camera resolution |
| CLOSED_EYES_DURATION_SECONDS | Drowsiness threshold |
| CLOSED_CONFIRMATION_FRAMES | False positive reduction |
| OPEN_CONFIRMATION_FRAMES | Eye reopening confirmation |

---

## Features Implemented

✔ Face Detection

✔ Eye Detection

✔ Temporal Eye State Tracking

✔ Real-time Monitoring Dashboard

✔ Alarm Thread

✔ Alert Counter

✔ Location Detection

✔ Configurable Parameters

---

## Current Limitations

- Uses Haar Cascade instead of deep learning models.
- Performance decreases under poor lighting.
- Glasses and occlusions may reduce accuracy.
- Single-person detection only.
- Requires webcam.

---

## Future Improvements

- MediaPipe Face Mesh
- Eye Aspect Ratio (EAR)
- YOLO Face Detection
- CNN-based Eye State Classification
- Yawning Detection
- Head Pose Estimation
- MobileNet / ResNet Integration
- Driver Attention Monitoring
- Performance Benchmarking
- Streamlit Dashboard

---

## Author

**Utkarsh Jaiswal**

M.Tech Computer Science

Indian Institute of Technology Guwahati

GitHub: https://github.com/Utkarsh-j03

---

## License

This project is licensed under the MIT License.
