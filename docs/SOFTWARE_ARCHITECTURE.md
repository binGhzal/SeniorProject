# Software Architecture

This document expands the software architecture beyond the high-level runtime pipeline in `docs/ARCHITECTURE.md`.

## Application software

### Main features

- [ ] Pair/connect to helmet
- [ ] Live dashboard (status + health)
- [ ] Alert center (crash/fatigue)
- [ ] History / trip reports

### Libraries and frameworks used

Placeholder (fill with actual choice):

- [ ] Mobile: (Flutter/React Native/Native)
- [ ] Web: (React/Vue/Svelte)
- [ ] Backend: (Python/Node/Go) if cloud exists

### UI design and UX principles

- [ ] Minimal rider distraction
- [ ] Clear prioritization of CRASH vs FATIGUE alerts
- [ ] Works offline (at least for viewing recent data)

## Embedded (board) software

### Firmware architecture

Current prototype is Python modules under `unit-tests/`.

For the target device, define:

- [ ] Runtime: Linux userspace vs RTOS vs bare metal
- [ ] Process/thread model: sensor polling, detection, telemetry
- [ ] Watchdog/health checks

### Libraries, drivers, middleware

- [x] Optional: OpenCV (camera on dev machine)
- [x] Optional: paho-mqtt (telemetry)
- [ ] IMU driver selection (smbus2/spidev/vendor)
- [ ] GPIO/PWM library (device-specific)

### Algorithms and processing logic

- [x] Crash detection: g-force magnitude threshold
- [x] Fatigue detection: EAR + rolling closed-eye buffer
- [ ] Face landmark extraction integration (MediaPipe or alternative)
- [ ] Filtering/calibration (IMU axis alignment, noise filtering)

### Programming language(s) and RTOS (if applicable)

- [x] Prototype: Python
- [ ] Target: (Python/C++/C) and (RTOS name if used)
