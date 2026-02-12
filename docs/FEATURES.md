# Feature Definition

This document defines GP2 features at two levels:

- **Application-level** features (mobile/web app)
- **On-board** features (embedded device / helmet)

Status: this tracks alignment between the original GP1 report scope and the implemented GP2 MVP.

## Scope alignment (GP1 \u2192 GP2)

- Implemented in GP2 MVP: fatigue detection (EAR/PERCLOS),
  crash detection (IMU high-g), MQTT status/alerts, local event buffering.
- Deferred from GP1 concept: EEG integration, distraction/head-pose analytics, cloud dashboard UX, circular video clip upload.

## Frozen platform scope

- Primary client platform: mobile application.
- Secondary platform: web dashboard for operations/review.
- MVP delivery focus: mobile-first with telemetry/event contracts shared with web.

## User stories and acceptance criteria

- US-01 Pair helmet - Given a known device identity, when pairing is requested, then the app stores the
  device profile and confirms connectivity.
- US-02 View live status - Given active telemetry, when status updates arrive, then fatigue/crash/health values
  render within one status interval.
- US-03 Receive crash alert - Given crash threshold crossing, when alert is emitted, then the alert center receives a
  CRASH event with timestamp and value.
- US-04 Receive fatigue alert - Given fatigue trigger, when alert is emitted, then the alert center receives a FATIGUE
  event with timestamp and EAR value.
- US-05 Review trip timeline - Given stored event records, when a trip is selected, then event and status summaries are
  listed chronologically.
- US-06 Configure thresholds - Given authorized settings access, when crash/fatigue thresholds are updated, then runtime
  configuration reflects validated values.
- US-07 Configure retention - Given storage settings, when retention is changed, then queue limits and retention window
  are enforced on subsequent cycles.
- US-08 Run events-only privacy mode - Given privacy mode enabled, when runtime publishes telemetry, then only minimal event
  payloads required for alerting are retained.
- US-09 Export user data - Given DSAR request, when export is triggered, then access-export output includes scoped
  trip/events/diagnostics records.
- US-10 Delete user data - Given DSAR delete request, when deletion is approved, then account-scoped records are
  removed per policy.

## MVP vs post-MVP matrix

| Feature                                       | Stage    | Traceability                                      |
| --------------------------------------------- | -------- | ------------------------------------------------- |
| Crash detection and alert publish             | MVP      | Runtime + tests in `tests/test_runtime.py`        |
| Fatigue detection and alert publish           | MVP      | Runtime + tests in `tests/test_runtime.py`        |
| Status telemetry with health/power/AI metrics | MVP      | `src/gp2/main.py` and telemetry payload tests     |
| Local queue retention + replay hooks          | MVP      | `storage_strategy.py` + replay/retention tests    |
| Connectivity recovery and retry ceiling       | MVP      | `telemetry.py` + reconnect/replay tests           |
| App schema and DSAR workflow contracts        | MVP      | `storage_strategy.py` schema/DSAR helpers + tests |
| Distraction detection execution pipeline      | Post-MVP | Planned contracts in AI/carry-forward docs        |
| Circular video event clips                    | Post-MVP | Planned clip metadata/workflow contracts          |
| Dashboard analytics UI                        | Post-MVP | Planned dashboard integration contract            |
| EEG-assisted fusion                           | Post-MVP | Deferred research scope from GP1                  |

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
- [x] **Sensor self-test** (startup checks + runtime health)

### Telemetry

- [x] **Periodic telemetry publish** (prototype: MQTT)
- [x] **Event alerts** (prototype: CRASH / FATIGUE)
- [x] **Local buffering** (SQLite retention + replay hooks)

### Device behavior

- [x] **IR illumination control** (PWM brightness interface)
- [ ] **Power modes** (active, standby, low-power)

### Board-side acceptance criteria

- Crash path
    - Runtime emits `CRASH` alert when total g-force exceeds threshold.
- Fatigue path
    - Runtime emits `FATIGUE` alert when detector reports drowsy state.
- Health path
    - Status telemetry includes sensor-health and runtime-health structures.
- Storage path
    - Local queue respects retention window and queue-size bounds.

## Open questions

- [ ] Target platform for the application: mobile, web, or both?
- [ ] Which alerts require immediate user action vs. silent logging?
- [ ] Who receives crash alerts (self only, emergency contact, cloud service)?
