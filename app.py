import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np
import cv2
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from diagnose import get_diagnosis

MODEL_PATH = r"runs\detect\pcb_detector\weights\best.pt"

st.set_page_config(page_title="PCB Fault Detector", page_icon="🔍", layout="wide")

st.title("🔍 PCB Fault Detection System")
st.markdown("Upload a PCB image to detect defects and get diagnostic information.")

@st.cache_resource
def load_model():
    return YOLO(MODEL_PATH)

model = load_model()

SEVERITY_COLOR = {
    'Critical': '🔴',
    'High':     '🟠',
    'Medium':   '🟡',
    'Low':      '🟢'
}

uploaded = st.file_uploader("Upload PCB Image", type=['jpg', 'jpeg', 'png'])

if uploaded:
    image = Image.open(uploaded).convert('RGB')
    img_array = np.array(image)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original Image")
        st.image(image, use_container_width=True)

    with st.spinner("Analyzing PCB..."):
        results = model(img_array, conf=0.25)
        result  = results[0]
        annotated = result.plot()
        annotated = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

    with col2:
        st.subheader("Detected Faults")
        st.image(annotated, use_container_width=True)

    boxes = result.boxes
    if boxes is None or len(boxes) == 0:
        st.success("✅ No faults detected — PCB looks healthy!")
    else:
        CLASS_NAMES = ['missing_hole', 'mouse_bite', 'open_circuit', 'short', 'spur', 'spurious_copper']
        detected = {}
        for box in boxes:
            cls_id = int(box.cls[0])
            cls_name = CLASS_NAMES[cls_id]
            conf = float(box.conf[0])
            if cls_name not in detected or detected[cls_name]['confidence'] < conf:
                detected[cls_name] = {'confidence': conf}

        st.subheader(f"Found {len(detected)} fault type(s)")

        for fault, info in detected.items():
            diag = get_diagnosis(fault)
            sev  = diag['severity']
            icon = SEVERITY_COLOR.get(sev, '⚪')

            with st.expander(f"{icon} {fault.replace('_', ' ').title()} — {sev} severity (conf: {info['confidence']:.0%})", expanded=True):
                st.markdown("**Consequence**")
                st.warning(diag['consequence'])
                st.markdown("**Solution**")
                st.success(diag['solution'])

        st.subheader("Summary")
        summary_data = []
        for fault, info in detected.items():
            diag = get_diagnosis(fault)
            summary_data.append({
                'Fault': fault.replace('_', ' ').title(),
                'Severity': diag['severity'],
                'Confidence': f"{info['confidence']:.0%}"
            })
        st.table(summary_data)