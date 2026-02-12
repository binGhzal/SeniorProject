# AI and Advanced Algorithms

This document describes the AI/ML components used by GP2.

Status: implemented with heuristic-first runtime mode and model-ready validation contracts.

## Description of AI-based features

- [x] Drowsiness detection from face/eye landmarks
- [ ] Optional: head pose / yawning / gaze estimation
- [ ] Optional: anomaly detection on IMU patterns

## Ready-to-use models vs. custom development

### Prototype path

- [x] Use ready-to-use landmark extractor (e.g., MediaPipe FaceMesh)
- [x] Apply custom logic (EAR/PERCLOS)
- [x] Expose algorithm mode selector (`heuristic-ear-perclos` vs `model-based`)

### Custom model path (optional)

- [ ] Train a classifier on features (EAR history, blink rate)
- [ ] Train an end-to-end model (video to drowsy) (higher risk/complexity)
- [x] Define model validation/evaluation contract fields for rollout gates

## Training data requirements

- [ ] Data sources: recorded videos (consented), public datasets
- [x] Labels: eyes-open/closed, drowsy episodes, lighting conditions
- [x] Diversity: users, skin tones, glasses, helmet fit

Current dataset scope and labeling taxonomy:

- Environments: `indoor_day`, `indoor_night`, `outdoor_day`, `outdoor_night`
- Subject buckets: `helmet_with_glasses`, `without_glasses`, `helmet_fit_variation`
- State labels: `eyes_open`, `eyes_closed`, `drowsy_episode`

## Data collection, training, validation, deployment strategy

- [ ] Collection protocol + consent
- [ ] Train/val/test split rules
- [x] Metrics: false alarm rate, detection latency (runtime fields added)
- [x] On-device deployment constraints (CPU, memory, power) captured in AI plan contract
- [x] Update strategy (model versioning) captured in `AIPlan.model_version`

Distraction-path validation protocol (planning contract):

- Signals: `gaze_offset`, `head_pitch`, `head_yaw`
- Trigger window: `2.0s`
- Thresholds: gaze offset `25°`, head pitch `20°`, head yaw `30°`
- Acceptance: max false-alert `0.05`, max detection latency `200ms`

### Baseline benchmark template

Use this template for each benchmark run:

- Run ID:
- Dataset tag:
- Runtime mode (`heuristic-ear-perclos` or `model-based`):
- Mean latency (ms):
- P95 latency (ms):
- False-alert rate:
- Miss rate:
- Device/profile:
- Notes:

### Rollout acceptance gates (go/no-go)

| Gate | Threshold | Decision rule |
| --- | --- | --- |
| Latency | `<= 200ms` alert path budget | No-go if exceeded in benchmark run |
| False alerts | `<= 0.05` | No-go if sustained above threshold |
| Runtime stability | No crash-loop regressions | No-go if reliability regresses |
| Resource bounds | Within CPU/memory/power budget | No-go if target budget exceeded |

## Phase 7 implementation summary

- AI planning module (`src/gp2/planning/ai_algorithms.py`) now provides:
    - `AIPlan` with dataset tag and rollout thresholds
    - `detector_mode(...)` for runtime mode selection
    - `evaluation_contract(...)` for dataset/metrics gate definitions
    - `supported_dataset_scopes()` for labeling buckets
- Fatigue runtime metrics now include `latency_ms`, `false_alert`, and `mode` fields.
