import gradio as gr
from ultralytics import YOLO
from PIL import Image
import numpy as np
import cv2
import os

os.environ["YOLO_CONFIG_DIR"] = "/tmp/Ultralytics"

DIAGNOSTICS = {
    'missing_hole': {
        'severity': 'Critical',
        'consequence': "Missing holes prevent component leads from being inserted and soldered, causing open circuits. In through-hole components like connectors or ICs, this means the component physically cannot be mounted, halting assembly entirely.",
        'solution': "Re-drill the missing hole using a CNC drill at the correct diameter specified in the PCB design file. Verify drill alignment against the Gerber file. After re-drilling, inspect pad integrity and re-plate if the annular ring is damaged."
    },
    'mouse_bite': {
        'severity': 'High',
        'consequence': "Mouse bites are irregular edge cuts that weaken the PCB mechanically and can sever edge traces or ground planes. This causes intermittent connections under vibration or thermal stress, leading to unpredictable field failures.",
        'solution': "If the mouse bite does not affect any trace, smooth the edge with a fine file and apply conformal coating to prevent oxidation. If a trace is severed, reroute using a wire bridge and secure with epoxy for mechanical strength."
    },
    'open_circuit': {
        'severity': 'Critical',
        'consequence': "An open circuit breaks the conductive path, meaning no current flows through that net. Depending on location this can disable an entire functional block — power delivery, signal lines, or ground return paths — rendering the board non-functional.",
        'solution': "Locate the break using a continuity tester or automated optical inspection. For thin trace breaks, apply conductive silver epoxy or solder a jumper wire across the gap. Re-inspect under magnification to confirm continuity restoration."
    },
    'short': {
        'severity': 'Critical',
        'consequence': "A short circuit creates an unintended low-resistance path between two nets, typically VCC and GND. This causes excessive current draw, overheating, and can permanently damage ICs, voltage regulators, or burn traces on the board.",
        'solution': "Identify the shorted nets using a multimeter in continuity mode before powering the board. Remove excess solder bridges using solder wick and flux. If the short is in copper pour, carefully scrape the unwanted copper with a precision knife and verify isolation with a multimeter."
    },
    'spur': {
        'severity': 'Medium',
        'consequence': "Spurs are unintended thin copper protrusions from a trace that can reduce clearance to adjacent traces. At high frequencies they act as antennas causing EMI issues, and under high voltage they risk dielectric breakdown and arcing.",
        'solution': "Remove the spur using a precision PCB router or sharp scalpel under magnification. After removal, clean the area with isopropyl alcohol and inspect the parent trace for damage. Apply conformal coating if the board operates in high-humidity environments."
    },
    'spurious_copper': {
        'severity': 'High',
        'consequence': "Spurious copper is unintended copper remaining after etching, which can create unintended short circuits between adjacent nets or reduce insulation resistance. On high-frequency boards it distorts impedance-controlled traces causing signal integrity issues.",
        'solution': "Carefully remove the spurious copper using a scalpel or micro-abrasive tool under a microscope. Verify electrical isolation with a hi-pot tester between affected nets. Review the etching process parameters to prevent recurrence in production."
    }
}

CLASS_NAMES = ['missing_hole', 'mouse_bite', 'open_circuit', 'short', 'spur', 'spurious_copper']

model = YOLO("runs/detect/pcb_detector/weights/best.pt")

def detect(image):
    img_array = np.array(image)
    results = model(img_array, conf=0.25)
    result = results[0]

    annotated = result.plot()
    annotated = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
    annotated_pil = Image.fromarray(annotated)

    boxes = result.boxes
    if boxes is None or len(boxes) == 0:
        return annotated_pil, "✅ No faults detected — PCB looks healthy!"

    detected = {}
    for box in boxes:
        cls_id = int(box.cls[0])
        cls_name = CLASS_NAMES[cls_id]
        conf = float(box.conf[0])
        if cls_name not in detected or detected[cls_name] < conf:
            detected[cls_name] = conf

    output = f"### Found {len(detected)} fault type(s)\n\n"
    for fault, conf in detected.items():
        diag = DIAGNOSTICS.get(fault, {})
        sev = diag.get('severity', 'Unknown')
        output += f"---\n"
        output += f"## {'🔴' if sev=='Critical' else '🟠' if sev=='High' else '🟡'} {fault.replace('_',' ').title()} — {sev} (conf: {conf:.0%})\n\n"
        output += f"**Consequence:**\n{diag.get('consequence','')}\n\n"
        output += f"**Solution:**\n{diag.get('solution','')}\n\n"

    return annotated_pil, output

demo = gr.Interface(
    fn=detect,
    inputs=gr.Image(type="pil", label="Upload PCB Image"),
    outputs=[
        gr.Image(type="pil", label="Detected Faults"),
        gr.Markdown(label="Diagnosis")
    ],
    title="PCB Fault Detection System",
    description="Upload a PCB image to detect defects and get circuit-level diagnostic information. Detects: Missing Hole, Mouse Bite, Open Circuit, Short Circuit, Spur, Spurious Copper.",
    examples=[]
)

demo.launch()