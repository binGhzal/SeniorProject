# Components

This is a file-by-file reference for the GP2 prototype.

## `src/gp2/main.py`

- Purpose: prototype orchestration loop that stitches together sensors,
  detection, and telemetry.
- Key behaviors:
    - Crash detection threshold: `total_g > 2.5`
    - Fatigue alert when `FatigueDetector` returns `drowsy=True`
    - Periodic `send_telemetry(perclos=..., g_force=...)`

## `src/gp2/sensors.py`

### `IMUSensor`

- `_init_sensor()` performs a soft reset (BMI160 style).
- `read_accel()` reads and converts raw accelerometer data to g’s.

Dev-machine behavior:

- If I2C libraries are missing, `IMUSensor` uses a small stub bus.
- Unit tests can monkeypatch the bus read call (`read_i2c_block_data`).

### `CameraModule`

- Uses OpenCV `VideoCapture` if OpenCV is installed.
- If OpenCV is missing, `get_frame()` returns `None`.

### `IRSys`

- Uses Raspberry Pi GPIO PWM if available.
- If GPIO libs are missing, calls are no-ops.

## `src/gp2/detection.py`

### `eye_aspect_ratio(eye)`

- Computes EAR using Euclidean distances between eye landmarks.

### `FatigueDetector`

- `analyze_frame(landmarks)`:
    - Splits the input landmarks into left/right eye slices using 68-point indices.
    - Computes average EAR.
    - Updates a rolling buffer of “closed eye” frames.
    - Returns drowsy state based on `PERCLOS_THRESH`.

Dev-machine behavior:

- If MediaPipe is not installed, the detector gracefully falls back to
  no-landmark mode.

### MediaPipe helpers

- `create_face_mesh()` builds an optional FaceMesh instance.
- `extract_face_landmarks(frame, face_mesh)` extracts landmarks from a frame
  when available.

## `src/gp2/telemetry.py`

### `TelemetryClient`

- Uses MQTT if `paho-mqtt` is installed.
- Provides:
    - `send_alert(alert_type, value)`
    - `send_telemetry(perclos, g_force)`

Dev-machine behavior:

- If MQTT library is not installed, the client initializes in a disabled mode
  and send methods become no-ops.

## `tests/test_runtime.py`

- Purpose: unit and “integration-style” tests.
- Covered behaviors:
    - IMU return format
    - Fatigue trigger behavior (via injected return)
    - Crash alert wiring (threshold → alert call)

For expected outputs and full run example, see `docs/TESTING.md`.

## `src/gp2/planning/`

- Purpose: task-aligned scaffolding modules created from `docs/tasks.md`.
- Scope: non-runtime placeholder classes/configs for:
    - features
    - hardware architecture
    - power plan
    - connectivity
    - storage strategy
    - software architecture
    - AI/algorithm planning

## `archive/legacy/`

- Purpose: archived or superseded runtime files kept for reference only.
- Current contents:
    - `sensors_rpi_only_legacy.py` (older sensor implementation previously
      named `sensons.py`)
- Rule: new work should target active modules under `src/gp2/` only.
