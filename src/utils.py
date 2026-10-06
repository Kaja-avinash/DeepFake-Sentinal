import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import streamlit as st
import mediapipe as mp

# --- PATHS ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# TensorFlow SavedModel folder
MODEL_PATH = os.path.join(BASE_DIR, "models", "final_model")

DATASET_REAL_PATH = os.path.join(BASE_DIR, "dataset", "processed_images", "real")

# --- INITIALIZE FACE DETECTOR ---
mp_face_detection = mp.solutions.face_detection
face_detector = mp_face_detection.FaceDetection(
    model_selection=0, min_detection_confidence=0.5
)


@st.cache_resource
def load_deepfake_model():
    if not os.path.exists(MODEL_PATH):
        st.error(f"MODEL NOT FOUND: {MODEL_PATH}")
        return None

    try:
        model = load_model(MODEL_PATH, compile=False)
        st.success("MODEL LOADED SUCCESSFULLY")
        return model

    except Exception as e:
        st.error(f"MODEL LOAD ERROR: {e}")
        return None


def preprocess_face(frame_bgr):
    try:
        h_img, w_img, _ = frame_bgr.shape

        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        results = face_detector.process(frame_rgb)

        if not results.detections:
            return None, None, None

        detection = results.detections[0]
        bbox = detection.location_data.relative_bounding_box

        x = int(bbox.xmin * w_img)
        y = int(bbox.ymin * h_img)
        w = int(bbox.width * w_img)
        h = int(bbox.height * h_img)

        p = 0.2
        x1 = max(0, int(x - w * p))
        y1 = max(0, int(y - h * p))
        x2 = min(w_img, int(x + w + w * p))
        y2 = min(h_img, int(y + h + h * p))

        face_crop_bgr = frame_bgr[y1:y2, x1:x2]
        face_resized = cv2.resize(face_crop_bgr, (224, 224))

        face_final = cv2.cvtColor(face_resized, cv2.COLOR_BGR2RGB) / 255.0
        face_batch = np.expand_dims(face_final, axis=0)

        return face_batch, (x, y, w, h), face_crop_bgr

    except:
        return None, None, None
