# 🖱️ Hand Gesture Controlled Virtual Mouse

This project is a Computer Vision-based system that allows users to control the mouse cursor using hand gestures.

## 🚀 Features
- Cursor movement using index finger
- Left click using thumb + index finger
- Drag functionality
- Right click using index + middle finger
- Smooth cursor movement using interpolation

## 🛠️ Technologies Used
- Python
- OpenCV
- MediaPipe
- PyAutoGUI
- NumPy

## 📷 How it Works
The system uses MediaPipe to detect 21 hand landmarks. The position of the index finger is mapped to screen coordinates for cursor movement. Different gestures are recognized based on the distance between fingers.

## ▶️ How to Run
```bash
pip install opencv-python mediapipe pyautogui numpy
python main.py
