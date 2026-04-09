import os
import glob
import xml.etree.ElementTree as ET
import shutil
import random

random.seed(42)

BASE = r"C:\Users\Prithviraj S\pcb-fault-detection\data\raw\PCB_DATASET"
OUT  = r"C:\Users\Prithviraj S\pcb-fault-detection\data"

CLASS_NAMES = ['missing_hole', 'mouse_bite', 'open_circuit', 'short', 'spur', 'spurious_copper']
CLASS_MAP   = {
    'Missing_hole':    0,
    'Mouse_bite':      1,
    'Open_circuit':    2,
    'Short':           3,
    'Spur':            4,
    'Spurious_copper': 5
}

for split in ['train', 'val', 'test']:
    os.makedirs(f"{OUT}/images/{split}", exist_ok=True)
    os.makedirs(f"{OUT}/labels/{split}", exist_ok=True)

all_data = []
for cls_folder, cls_id in CLASS_MAP.items():
    ann_folder = os.path.join(BASE, 'Annotations', cls_folder)
    img_folder = os.path.join(BASE, 'images', cls_folder)
    xml_files  = glob.glob(os.path.join(ann_folder, '*.xml'))
    for xml_path in xml_files:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        size = root.find('size')
        W = int(size.find('width').text)
        H = int(size.find('height').text)
        yolo_lines = []
        for obj in root.findall('object'):
            name = obj.find('name').text.strip()
            cid  = CLASS_MAP.get(name, cls_id)
            bb   = obj.find('bndbox')
            x1   = float(bb.find('xmin').text)
            y1   = float(bb.find('ymin').text)
            x2   = float(bb.find('xmax').text)
            y2   = float(bb.find('ymax').text)
            cx   = ((x1+x2)/2)/W
            cy   = ((y1+y2)/2)/H
            w    = (x2-x1)/W
            h    = (y2-y1)/H
            yolo_lines.append(f"{cid} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}")
        stem    = os.path.splitext(os.path.basename(xml_path))[0]
        img_path = os.path.join(img_folder, stem + '.jpg')
        if os.path.exists(img_path) and yolo_lines:
            all_data.append((img_path, yolo_lines))

random.shuffle(all_data)
n     = len(all_data)
train = all_data[:int(0.7*n)]
val   = all_data[int(0.7*n):int(0.85*n)]
test  = all_data[int(0.85*n):]

for split, items in [('train',train),('val',val),('test',test)]:
    for img_path, yolo_lines in items:
        fname = os.path.basename(img_path)
        shutil.copy(img_path, f"{OUT}/images/{split}/{fname}")
        lbl_name = fname.replace('.jpg', '.txt')
        with open(f"{OUT}/labels/{split}/{lbl_name}", 'w') as f:
            f.write('\n'.join(yolo_lines))

print(f"Done! Train: {len(train)}, Val: {len(val)}, Test: {len(test)}")