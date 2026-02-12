# Software Architecture

This document expands the software architecture beyond the high-level runtime pipeline in `docs/ARCHITECTURE.md`.

Status: implemented for MVP orchestration contract and side-effect boundary separation.

## Application software

### Main features

- [x] Pair/connect to helmet
- [x] Live dashboard (status + health)
- [x] Alert center (crash/fatigue)
- [ ] History / trip reports

### Libraries and frameworks used

Current stack choices:

- [ ] Mobile: deferred (out of runtime prototype scope)
- [ ] Web: deferred (out of runtime prototype scope)
- [x] Backend/runtime: Python (`src/gp2`)
- [x] Runtime dependencies declared in `src/gp2/planning/software_architecture.py`

### UI design and UX principles

- [ ] Minimal rider distraction
- [ ] Clear prioritization of CRASH vs FATIGUE alerts
- [ ] Works offline (at least for viewing recent data)

## Embedded (board) software

### Firmware architecture

Current prototype runtime is packaged under `src/gp2/` with tests in `tests/`.

Current runtime model:

- [x] Runtime: Linux userspace prototype
- [x] Process/thread model: single-thread polling with inline detection and telemetry
- [x] Orchestrator contract for one cycle in `execute_runtime_cycle(...)`
- [ ] Watchdog/health checks (planned)

### Libraries, drivers, middleware

- [x] Optional: OpenCV (camera on dev machine)
- [x] Optional: paho-mqtt (telemetry)
- [ ] IMU driver selection (smbus2/spidev/vendor)
- [ ] GPIO/PWM library (device-specific)

### Algorithms and processing logic

- [x] Crash detection: g-force magnitude threshold
- [x] Fatigue detection: EAR + rolling closed-eye buffer
- [x] Runtime contract output includes fatigue mode, latency, and false-alert metadata
- [ ] Face landmark extraction integration (MediaPipe or alternative)
- [ ] Filtering/calibration (IMU axis alignment, noise filtering)

### Programming language(s) and RTOS (if applicable)

- [x] Prototype: Python
- [ ] Target: (Python/C++/C) and (RTOS name if used)

## Phase 6 implementation summary

- Single-cycle orchestrator contract and execution path:
  - `RuntimeOrchestratorContract`
  - `execute_runtime_cycle(...)`
- Side-effect boundary ownership map in `side_effect_boundaries()`.
- Dependency declaration helper in `dependency_versions()`.
