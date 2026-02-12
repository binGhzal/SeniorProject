# Architecture

GP2 is a prototype “smart helmet” loop that combines:

- **Fatigue detection** (EAR + PERCLOS-style rolling window)
- **Crash detection** (high-G threshold from IMU)
- **Telemetry** (MQTT status + alert topics)

## Directory layout

- `perclos.py`
  - Reference snippet for MediaPipe FaceMesh initialization (eye/iris landmarks).
- `unit-tests/`
  - Prototype runtime loop and testable modules.

## Runtime pipeline

### 1) Sensors

Implemented in `unit-tests/sensors.py`.

- **IMU (`IMUSensor`)**
  - Reads 6 bytes from an accelerometer register block and converts to `(ax, ay, az)` in g’s.
- **Camera (`CameraModule`)**
  - Captures frames via OpenCV `VideoCapture`.
- **IR (`IRSys`)**
  - Controls IR LED brightness through PWM.

On non-Raspberry Pi machines, `sensors.py` includes safe fallbacks so the module can still be imported and unit tests can run without hardware.

### 2) Detection

Implemented in `unit-tests/detection.py`.

- **EAR (Eye Aspect Ratio)**
  - Computes an eye openness measure from 6 eye landmarks.
- **Rolling closed-eye score (PERCLOS-like)**
  - Tracks a rolling buffer of closed-eye frames.
  - Triggers fatigue when `perclos_score > PERCLOS_THRESH`.

Inputs/outputs:

- Input: an array/list of facial landmarks (68-point indexing assumed in this prototype)
- Output: `(is_drowsy: bool, ear: float)`

### 3) Crash detection

Implemented in the orchestration loop (`unit-tests/main.py`).

- Computes total acceleration magnitude:
  - $total_g = \sqrt{a_x^2 + a_y^2 + a_z^2}$
- Triggers crash if `total_g > 2.5`.

### 4) Telemetry

Implemented in `unit-tests/telemetry.py`.

- **Topics**
  - Telemetry: `smarthelmet/v1/telemetry`
  - Alerts: `smarthelmet/v1/alerts`
- **Payloads**
  - Status: includes `perclos` and `g_force`.
  - Alert: includes `alert` type and `value`.

MQTT is treated as an optional dependency so the code can import in environments without `paho-mqtt`.

## Orchestration

The prototype loop is in `unit-tests/main.py`:

1. Initialize sensors, telemetry, detector
2. In a loop:
   - Read IMU and compute `total_g`
   - If crash threshold exceeded: publish `CRASH` alert
   - Get camera frame (if available)
   - Run fatigue detector (prototype uses mock landmarks)
   - If fatigue condition triggered: publish `FATIGUE` alert
   - Send periodic status telemetry

## Key design assumptions (prototype)

- Facial landmarks are assumed to be 68-point indices (dlib-style). MediaPipe FaceMesh uses a different indexing scheme; `perclos.py` is a starting point but not integrated.
- The fatigue test suite focuses on **logic trigger and integration wiring**, not accuracy/validation against real video.
