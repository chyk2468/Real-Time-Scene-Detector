import streamlit as st
import cv2
import os
import numpy as np
from PIL import Image
from model import model, guess_scene  # Import model and guess_scene directly

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Real-time Scene Vision",
    page_icon="🤖",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

body { background-color: #000000; font-family: 'Outfit', sans-serif; color: #f8fafc; }
.stApp { background: radial-gradient(circle at 50% 10%, #1e1b4b 0%, #020617 60%, #000000 100%); background-attachment: fixed; }
.hero-title { font-size: 40px; font-weight: 800; text-align: center; background: linear-gradient(to right, #60a5fa, #c084fc, #f472b6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 20px; }
.obj-pill { display: flex; justify-content: space-between; padding: 6px 10px; background: rgba(255, 255, 255, 0.05); border-radius: 8px; margin-bottom: 4px; border: 1px solid rgba(255, 255, 255, 0.1); }
.scene-badge { display: inline-block; padding: 4px 12px; border-radius: 50px; background: linear-gradient(90deg, #2563eb, #7c3aed); color: white; font-weight: 600; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='hero-title'>AI Real-time Scene Vision</div>", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    mode = st.radio("Choose Mode", ["Real-time Stream", "Upload / Snapshot"])
    conf_threshold = st.slider("Confidence Threshold", 0.1, 1.0, 0.4)
    st.divider()
    st.info("Real-time mode uses your local webcam for continuous detection.")

# ---------------- MAIN UI ----------------
if mode == "Real-time Stream":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📹 Live Feed")
        run = st.checkbox('Start Camera', value=True)
        frame_placeholder = st.empty()
    
    with col2:
        st.markdown("### 📊 Live Analytics")
        scene_placeholder = st.empty()
        list_placeholder = st.empty()

    if run:
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        frame_count = 0
        object_counts = {}
        scene = "Detecting..."

        while cap.isOpened() and run:
            ret, frame = cap.read()
            if not ret: break

            # 🚀 OPTIMIZATION: Only process every 3rd frame
            if frame_count % 3 == 0:
                # Resize for faster inference
                results = model(frame, conf=conf_threshold, verbose=False, imgsz=320)
                
                # Update counts
                object_counts = {}
                for box in results[0].boxes:
                    label = model.names[int(box.cls[0])]
                    object_counts[label] = object_counts.get(label, 0) + 1
                
                scene = guess_scene(object_counts)
                annotated_frame = results[0].plot()
                
                # Update UI elements only when AI runs
                frame_placeholder.image(annotated_frame, channels="BGR", use_column_width=True)
                scene_placeholder.markdown(f"<div class='scene-badge'>📍 {scene}</div>", unsafe_allow_html=True)
                
                with list_placeholder.container():
                    if object_counts:
                        for k, v in object_counts.items():
                            st.markdown(f"<div class='obj-pill'><span>{k.title()}</span><b>{v}</b></div>", unsafe_allow_html=True)
                    else:
                        st.write("Detecting objects...")

            frame_count += 1
            if not run: break
        
        cap.release()
    else:
        st.warning("Camera is stopped.")

else:
    # --- ORIGINAL UPLOAD LOGIC ---
    from model import detect_and_guess_scene
    
    main_col1, main_col2 = st.columns([1, 1], gap="large")
    with main_col1:
        st.markdown("### 📥 Input Dialog")
        uploaded_file = st.file_uploader("Upload Image File", type=["jpg", "jpeg", "png"])
        analyze_btn = st.button("✨ START AI ANALYSIS", type="primary", use_container_width=True)

    with main_col2:
        st.markdown("### 📸 Snapshot")
        camera_file = st.camera_input("Capture Scene", label_visibility="collapsed")

    source_file = uploaded_file if uploaded_file else camera_file

    if source_file:
        os.makedirs("outputs", exist_ok=True)
        file_name = getattr(source_file, "name", "camera_shot.jpg")
        input_path = os.path.join("outputs", file_name)
        output_path = os.path.join("outputs", "detected_" + file_name)

        with open(input_path, "wb") as f:
            f.write(source_file.getbuffer())

        if analyze_btn:
            with st.spinner("🤖 Analyzing..."):
                objects, scene, out_img = detect_and_guess_scene(input_path, output_path)
                st.divider()
                res_col1, res_col2 = st.columns([2, 1])
                with res_col1:
                    st.image(out_img, caption=f"Detected Scene: {scene}", use_column_width=True, channels="BGR")
                with res_col2:
                    st.markdown(f"#### 📍 Scene: `{scene}`")
                    if objects:
                        for k, v in objects.items():
                            st.markdown(f"<div class='obj-pill'><span>{k.title()}</span><b>{v}</b></div>", unsafe_allow_html=True)
        else:
            st.image(input_path, width=300)
