import tensorflow as tf  # <--- MUST BE THE VERY FIRST IMPORT
import cv2
import mediapipe as mp
import numpy as np

# ... rest of the test_dl.py code ...

# Initialize Deep Learning Face Detector
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

# Initialize Camera
cap = cv2.VideoCapture(0)
print("📸 Testing Neural Face Detection... Press 'q' to exit.")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Neural Detector expects RGB images
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb_frame)

    # Draw Neural Detections
    if results.detections:
        for detection in results.detections:
            # Drawing utilities for visual confirmation
            mp.solutions.drawing_utils.draw_detection(frame, detection)
            print("👤 Face Detected by Neural Network!")

    cv2.imshow("DL Detection Test", frame)
    if cv2.waitKey(5) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
