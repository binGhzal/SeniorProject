# Feature Definition

This document defines GP2 features at two levels:

- **Application-level** features (mobile/web app)
- **On-board** features (embedded device / helmet)

Status: this tracks alignment between the original GP1 report scope and the implemented GP2 MVP.

## Scope alignment (GP1 \u2192 GP2)

- Implemented in GP2 MVP: fatigue detection (EAR/PERCLOS),
  crash detection (IMU high-g), MQTT status/alerts, local event buffering.
- Deferred from GP1 concept: EEG integration, distraction/head-pose analytics, cloud dashboard UX, circular video clip upload.

## Application-level features (mobile/web)

### Core user features

- [ ] **Pair device** (discover + connect to helmet)
- [x] **Live status** (fatigue state + crash state + sensor health) via telemetry payloads
- [x] **Alerts** (event alerts over telemetry topics)
- [ ] **Trip history** (timeline of telemetry summaries)

### Configuration

- [ ] **Threshold tuning** (EAR/PERCLOS, crash g-force)
- [ ] **Device settings** (device_id, sampling rates, data retention)

### UX principles (placeholder)

- [ ] Minimal interaction while riding
- [ ] Clear “action” guidance for alerts
- [ ] Accessibility: large typography, high contrast, hands-free-friendly

## On-board features (embedded device)

### Safety detection

- [x] **Crash detection** (prototype: high-g threshold)
- [x] **Fatigue detection** (prototype: EAR + rolling PERCLOS-like score)
- [ ] **Sensor self-test** (startup checks + runtime health)

### Telemetry

- [x] **Periodic telemetry publish** (prototype: MQTT)
- [x] **Event alerts** (prototype: CRASH / FATIGUE)
- [x] **Local buffering** (SQLite retention + replay hooks)

### Device behavior

- [x] **IR illumination control** (PWM brightness interface)
- [ ] **Power modes** (active, standby, low-power)

## Open questions

- [ ] Target platform for the application: mobile, web, or both?
- [ ] Which alerts require immediate user action vs. silent logging?
- [ ] Who receives crash alerts (self only, emergency contact, cloud service)?
