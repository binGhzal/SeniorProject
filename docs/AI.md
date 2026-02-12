# AI and Advanced Algorithms

This document describes the AI/ML components (if any) used by GP2.

Status: placeholder; current prototype uses classical geometric features (EAR/PERCLOS) and thresholding.

## Description of AI-based features

- [ ] Drowsiness detection from face/eye landmarks
- [ ] Optional: head pose / yawning / gaze estimation
- [ ] Optional: anomaly detection on IMU patterns

## Ready-to-use models vs. custom development

### Prototype path

- [x] Use ready-to-use landmark extractor (e.g., MediaPipe FaceMesh)
- [x] Apply custom logic (EAR/PERCLOS)

### Custom model path (optional)

- [ ] Train a classifier on features (EAR history, blink rate)
- [ ] Train an end-to-end model (video  drowsy) (higher risk/complexity)

## Training data requirements

- [ ] Data sources: recorded videos (consented), public datasets
- [ ] Labels: eyes-open/closed, drowsy episodes, lighting conditions
- [ ] Diversity: users, skin tones, glasses, helmet fit

## Data collection, training, validation, deployment strategy

- [ ] Collection protocol + consent
- [ ] Train/val/test split rules
- [ ] Metrics: false alarm rate, detection latency
- [ ] On-device deployment constraints (CPU, memory, power)
- [ ] Update strategy (model versioning)
