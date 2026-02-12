# Feature Definition

This document defines GP2 features at two levels:

- **Application-level** features (mobile/web app)
- **On-board** features (embedded device / helmet)

Status: these are **requirements placeholders** aligned with the project prototype described in `docs/ARCHITECTURE.md`.

## Application-level features (mobile/web)

### Core user features

- [ ] **Pair device** (discover + connect to helmet)
- [ ] **Live status** (fatigue state + crash state + sensor health)
- [ ] **Alerts** (push/notification + in-app alert list)
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
- [ ] **Local buffering** (queue telemetry while offline)

### Device behavior

- [ ] **IR illumination control** (for low light camera)
- [ ] **Power modes** (active, standby, low-power)

## Open questions

- [ ] Target platform for the application: mobile, web, or both?
- [ ] Which alerts require immediate user action vs. silent logging?
- [ ] Who receives crash alerts (self only, emergency contact, cloud service)?
