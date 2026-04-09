# PCB Fault Detection System

An AI-powered system for automated detection and diagnosis of Printed Circuit Board (PCB) defects using YOLOv8 deep learning.

## Overview

This project implements a two-stage pipeline:
1. **Detection** — YOLOv8 model trained to localize and classify 6 types of PCB defects
2. **Diagnosis** — ECE-informed reasoning layer that maps each detected fault to its circuit-level consequence and repair solution

## Detected Fault Classes

| Fault | Severity |
|-------|----------|
| Missing Hole | Critical |
| Mouse Bite | High |
| Open Circuit | Critical |
| Short Circuit | Critical |
| Spur | Medium |
| Spurious Copper | High |

## Results

Trained on the PCB Defects Dataset (Kaggle) — 693 images, 6 defect classes.

| Metric | Score |
|--------|-------|
| Overall mAP50 (test) | 86.5% |
| Missing Hole mAP50 | 98.2% |
| Short Circuit mAP50 | 94.6% |
| Mouse Bite mAP50 | 90.8% |
| Spurious Copper mAP50 | 87.2% |
| Open Circuit mAP50 | 83.0% |
| Spur mAP50 | 65.5% |

*Trained on CPU only (Intel i5-1235U) — no GPU used.*

## Tech Stack

- Python 3.12
- YOLOv8 (Ultralytics)
- OpenCV
- Streamlit
- PyTorch

## Project Structure