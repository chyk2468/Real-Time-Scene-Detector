# 🤖 AI Real-time Scene Vision

AI Real-time Scene Vision is a modern, high-performance computer vision application that detects objects in real-time and intelligently "guesses" the scene context (e.g., Office, Kitchen, Street) based on the detected items. Built with **Streamlit** and **YOLOv8**, it offers a sleek, dark-themed interface for both live camera feeds and static image analysis.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLOv8-00A9E0?style=for-the-badge&logo=ultralytics&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)

---

## ✨ Features

- **📹 Real-time Stream:** Continuous object detection from your webcam with optimized frame processing (every 3rd frame) for a smooth experience.
- **📸 Upload & Snapshot:** Analyze existing image files or take a quick snapshot using your camera.
- **📍 Scene Guessing:** An intelligent heuristic engine that categorizes the environment into scenes like *Office, Kitchen, Living Room, Street, Market,* etc.
- **📊 Live Analytics:** Real-time breakdown of detected objects and counts displayed in a clean, modern UI.
- **🎨 Custom Dark UI:** A polished interface featuring custom CSS, radial gradients, and "glassmorphism" inspired UI elements.

---

## 🛠️ Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)
- **Model:** [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) (PyTorch/ONNX)
- **Image Processing:** [OpenCV](https://opencv.org/) & [Pillow](https://python-pillow.org/)
- **Language:** Python 3.x

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd project
```

### 2. Install Dependencies
Make sure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
streamlit run app.py
```

---

## 📖 Usage

1. **Launch the app** via the command above.
2. **Settings Sidebar:** Choose between "Real-time Stream" or "Upload / Snapshot" mode. Adjust the **Confidence Threshold** to filter out weak detections.
3. **Real-time Mode:** Check "Start Camera" to begin. The app will label objects and update the "Live Analytics" panel automatically.
4. **Upload Mode:** Drag and drop an image or use the "Capture Scene" button. Click **✨ START AI ANALYSIS** to process.

---

## 🧠 How It Works

1. **Object Detection:** The app uses a YOLOv8 model (`model.pt`) trained on the COCO dataset to identify 80+ common object classes.
2. **Inference Optimization:** In real-time mode, only every 3rd frame is processed by the AI to reduce CPU/GPU load while maintaining a responsive UI.
3. **Heuristic Scene Engine:** The `guess_scene` function in `model.py` analyzes the frequency and type of objects detected. For example:
   - `Laptop + Mouse + Chair` ➔ **Office**
   - `Microwave + Sink + Refrigerator` ➔ **Kitchen**
   - `Cars + Traffic Lights` ➔ **Street**

---

## 📁 Project Structure

```text
C:\Users\91630\Desktop\project\
├───app.py              # Main Streamlit application & UI
├───model.py            # AI logic and scene guessing heuristics
├───model.pt            # YOLOv8 weights (PyTorch)
├───requirements.txt    # Project dependencies
├───outputs\            # Saved images from analysis
└───Sample images\      # Test images for demonstration
```

---

## 🛠️ Future Improvements

- [ ] Support for more specific scene models (e.g. Places365).
- [ ] Option to switch between different YOLO models (Nano, Small, Large).
- [ ] Export analysis reports to PDF/CSV.
- [ ] Integration with cloud storage for saving detection history.

---

Developed with ❤️ using Python and Streamlit.
