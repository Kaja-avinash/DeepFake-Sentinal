import streamlit as st
import cv2
import numpy as np
import time
import os
import tempfile
import textwrap
from datetime import datetime

# Import modules
from styles import inject_custom_css
from utils import load_deepfake_model, preprocess_face, DATASET_REAL_PATH

# --- CONFIGURATION ---
st.set_page_config(
    page_title="REALITY OPS",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_custom_css()
model = load_deepfake_model()
if model is None:
    st.stop()

# --- SESSION STATE ---
if "current_mode" not in st.session_state:
    st.session_state["current_mode"] = "LIVE SCANNER"

# --- STELLAR VORTEX BACKGROUND ---
st.markdown(
    """
<div class="stellar-vortex-container">
<div class="vortex-cloud"></div>
<div class="vortex-stars"></div>
<div class="vortex-core"></div>
</div>
""",
    unsafe_allow_html=True,
)

# --- HEADER ---
st.markdown(
    """
<div style="text-align: center; padding-top: 20px; padding-bottom: 20px; position: relative; z-index: 2;">
<h1 style="font-size: 3.5rem; margin-bottom: 5px;">REALITY <span style="color:#00f3ff;">OPS</span></h1>
<p style="font-size: 0.9rem; letter-spacing: 4px; color: #546e7a; margin: 0; text-transform:uppercase;">
Tactical Biometric Forensics
</p>
</div>
""",
    unsafe_allow_html=True,
)

# --- NAV BAR ---
selected_mode = st.radio(
    "",
    ["LIVE SCANNER", "IMAGE FORENSICS", "VIDEO ANALYSIS", "DATA CAPTURE"],
    horizontal=True,
    label_visibility="collapsed",
)

# --- TRANSITION LOGIC ---
if selected_mode != st.session_state["current_mode"]:
    placeholder = st.empty()

    loading_html = textwrap.dedent(f"""
    <div class="loader-overlay">
    <div class="stellar-vortex-container">
    <div class="vortex-cloud"></div>
    <div class="vortex-stars"></div>
    <div class="vortex-core"></div>
    </div>
    <div class="loader-box">
    <svg width="120" height="120" viewBox="0 0 100 100">
    <circle cx="50" cy="50" r="45" stroke="#00f3ff" stroke-width="2" fill="none" stroke-dasharray="210 30" opacity="0.5">
    <animateTransform attributeName="transform" type="rotate" from="0 50 50" to="360 50 50" dur="4s" repeatCount="indefinite" />
    </circle>
    <circle cx="50" cy="50" r="35" stroke="#00f3ff" stroke-width="2" fill="none" stroke-dasharray="150 20">
    <animateTransform attributeName="transform" type="rotate" from="360 50 50" to="0 50 50" dur="2s" repeatCount="indefinite" />
    </circle>
    <path d="M50 25 C35 25 25 35 25 50 C25 70 35 85 50 85 C65 85 75 70 75 50 C75 35 65 25 50 25" fill="none" stroke="#00f3ff" stroke-width="2" stroke-dasharray="200">
    <animate attributeName="stroke-dashoffset" values="200;0" dur="1.5s" repeatCount="indefinite" />
    </path>
    <line x1="20" y1="50" x2="80" y2="50" stroke="#00f3ff" stroke-width="2" opacity="0.8">
    <animate attributeName="y1" values="25;85;25" dur="1.5s" repeatCount="indefinite" />
    <animate attributeName="y2" values="25;85;25" dur="1.5s" repeatCount="indefinite" />
    </line>
    </svg>
    <div class="loading-text">INITIALIZING {selected_mode}</div>
    <div class="loading-bar"><div class="loading-bar-fill"></div></div>
    </div>
    </div>
    """)

    with placeholder.container():
        st.markdown(loading_html, unsafe_allow_html=True)

    time.sleep(2.5)
    placeholder.empty()
    st.session_state["current_mode"] = selected_mode

app_mode = st.session_state["current_mode"]

# ==========================================
# 1. LIVE SCANNER
# ==========================================
if app_mode == "LIVE SCANNER":
    st.markdown(
        """
        <div class="neon-card">
            <h2>🔴 LIVE SURVEILLANCE</h2>
            <p>Real-time deepfake detection feed. Secure connection established.</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([3, 1])

    with col1:
        frame_window = st.image([])

    with col2:
        st.markdown(
            "**STATUS:** <span style='color:#00f3ff'>STANDBY</span>",
            unsafe_allow_html=True,
        )

        if st.button("ACTIVATE CAMERA"):
            st.markdown(
                "**STATUS:** <span style='color:#ff2a2a'>SCANNING</span>",
                unsafe_allow_html=True,
            )

            cap = cv2.VideoCapture(0)
            img_container = st.empty()
            stop_button = st.button("STOP FEED")

            while not stop_button:
                ret, frame = cap.read()
                if not ret:
                    break

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Single face preprocessing
                inp, coords, _ = preprocess_face(frame)

                if inp is not None:
                    pred = model.predict(inp, verbose=0)[0][0]
                    x, y, w, h = coords

                    REAL_MIN_CONF = 0.60

                    if pred >= REAL_MIN_CONF:
                        is_fake = False
                        conf = pred
                    else:
                        is_fake = True
                        conf = 1 - pred

                    color = (255, 0, 0) if is_fake else (0, 255, 0)
                    label = (
                        f"FAKE: {conf * 100:.1f}%"
                        if is_fake
                        else f"REAL: {conf * 100:.1f}%"
                    )

                    cv2.rectangle(frame_rgb, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(
                        frame_rgb,
                        label,
                        (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        color,
                        2,
                    )

                frame_window.image(frame_rgb, use_container_width=True)

            cap.release()

# ==========================================
# 2. IMAGE FORENSICS
# ==========================================
elif app_mode == "IMAGE FORENSICS":
    st.markdown(
        """
        <div class="neon-card">
            <h2>📂 STATIC ANALYSIS</h2>
            <p>Upload suspect media for artifact inspection.</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    f = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    if f:
        file_bytes = np.asarray(bytearray(f.read()), dtype=np.uint8)
        img_bgr = cv2.imdecode(file_bytes, 1)
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

        c1, c2 = st.columns(2)

        with c1:
            st.image(img_rgb, caption="SOURCE", use_container_width=True)

        with c2:
            if st.button("RUN DIAGNOSTICS"):
                with st.spinner("ANALYZING..."):
                    time.sleep(1)

                    inp, coords, _ = preprocess_face(img_bgr)

                    if inp is not None:
                        pred = model.predict(inp, verbose=0)[0][0]
                        x, y, w, h = coords

                        REAL_MIN_CONF = 0.85  # strict authenticity rule

                        if pred >= REAL_MIN_CONF:
                            is_fake = False
                            conf = pred
                        else:
                            is_fake = True
                            conf = 1 - pred

                        if is_fake:
                            st.error(f"FAKE DETECTED ({conf * 100:.1f}%)")
                            cv2.rectangle(
                                img_rgb, (x, y), (x + w, y + h), (255, 0, 0), 3
                            )
                        else:
                            st.success(f"AUTHENTIC ({conf * 100:.1f}%)")
                            cv2.rectangle(
                                img_rgb, (x, y), (x + w, y + h), (0, 255, 0), 3
                            )

                        st.image(img_rgb, caption="RESULT", use_container_width=True)

                    else:
                        st.warning("NO FACE DETECTED")


# ==========================================
# 3. VIDEO ANALYSIS
# ==========================================
elif app_mode == "VIDEO ANALYSIS":
    st.markdown(
        """
        <div class="neon-card">
            <h2>🎞️ NEURAL VIDEO FORENSICS</h2>
            <p>Performing frame-by-frame deep learning verification.</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    src = st.radio("SOURCE", ["FILE UPLOAD", "DIRECT URL"], horizontal=True)
    cap = None

    if src == "FILE UPLOAD":
        v = st.file_uploader("Upload Video", type=["mp4", "avi", "mov"])
        if v:
            t = tempfile.NamedTemporaryFile(delete=False)
            t.write(v.read())
            cap = cv2.VideoCapture(t.name)
            # st.video(v) # Optional: remove this if you want only the "Neural View"
    else:
        u = st.text_input("Direct Video URL (e.g. .mp4 / .mkv)")
        if u:
            cap = cv2.VideoCapture(u)

    if cap and st.button("EXECUTE NEURAL SCAN"):
        # Placeholder for real-time visual feedback
        video_placeholder = st.empty()
        bar = st.progress(0)
        preds = []

        # Get video properties
        tot = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if tot <= 0:
            tot = 100  # Fallback for some URLs

        curr = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Process every 10th frame (Performance Balancing)
            if curr % 10 == 0:
                # 100% DL Preprocessing (MediaPipe + Attention Model)
                inp, coords, _ = preprocess_face(frame)

                if inp is not None:
                    # Neural Prediction
                    pred = model.predict(inp, verbose=0)[0][0]
                    preds.append(pred)

                    # DRAWING: Show the user what the AI sees
                    x, y, w, h = coords
                    color = (255, 0, 0) if pred < 0.5 else (0, 255, 0)  # Red if Fake
                    label = "SUSPECT" if pred < 0.5 else "AUTHENTIC"

                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 4)
                    cv2.putText(
                        frame,
                        f"{label} {pred * 100:.1f}%",
                        (x, y - 15),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        color,
                        2,
                    )

                # Convert BGR to RGB for Streamlit Display
                video_placeholder.image(
                    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), use_container_width=True
                )

            curr += 1
            bar.progress(min(curr / tot, 1.0))

        cap.release()

        # --- FINAL VERDICT ---
        if preds:
            avg = np.mean(preds)
            st.markdown("---")
            if avg > 0.5:
                st.error(f"🚨 FINAL VERDICT: FAKE DETECTED ({avg * 100:.1f}%)")
                st.warning("Forensic artifacts found in facial movements and textures.")
            else:
                st.success(f"✅ FINAL VERDICT: AUTHENTIC ({(1 - avg) * 100:.1f}%)")
                st.info("Biometric markers appear consistent with real human media.")

# ==========================================
# 4. DATA CAPTURE
# ==========================================
elif app_mode == "DATA CAPTURE":
    st.markdown(
        """
        <div class="neon-card">
            <h2>📡 DATA COLLECTION</h2>
            <p>Capture labeled data for model retraining.</p>
        </div>
    """,
        unsafe_allow_html=True,
    )
    if not os.path.exists(DATASET_REAL_PATH):
        os.makedirs(DATASET_REAL_PATH)

    col1, col2 = st.columns(2)
    with col2:
        if st.button("START BATCH CAPTURE"):
            cap = cv2.VideoCapture(0)
            win = st.image([])
            bar = st.progress(0)
            cnt = 0
            while cnt < 50:
                ret, frame = cap.read()
                if not ret:
                    break

                # Frame is BGR
                inp, coords, crop_bgr = preprocess_face(frame)

                if crop_bgr is not None:
                    # Save BGR image (OpenCV default)
                    n = f"cap_{datetime.now().strftime('%M%S%f')}.jpg"
                    cv2.imwrite(os.path.join(DATASET_REAL_PATH, n), crop_bgr)

                    cnt += 1

                    # Display Feedback (Convert to RGB)
                    x, y, w, h = coords
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    cv2.rectangle(frame_rgb, (x, y), (x + w, y + h), (0, 243, 255), 2)
                    win.image(frame_rgb, use_container_width=True)

                bar.progress(int((cnt / 50) * 100))
                time.sleep(0.05)
            cap.release()
            st.success("Capture Complete")
