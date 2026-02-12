# Setup & Dependencies

This project is a prototype that can be developed and tested on macOS/Windows/Linux, with optional Raspberry Pi hardware support.

## Python environment

Recommended: use a virtual environment.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

## Minimal dependencies (unit tests)

Unit tests require `numpy`:

```bash
python -m pip install numpy
```

Run tests:

```bash
python -m unittest tests/test_runtime.py -v
```

## Optional dependencies (runtime)

### MQTT telemetry

Install MQTT client library:

```bash
python -m pip install paho-mqtt
```

### Camera on laptop/desktop

Install OpenCV:

```bash
python -m pip install opencv-python
```

### Face landmarks

MediaPipe FaceMesh is integrated in `src/gp2/detection.py` for frame-based landmark extraction. To enable it:

```bash
python -m pip install mediapipe opencv-python
```

### Raspberry Pi hardware libraries

On Raspberry Pi OS, you may need (package names vary by distro/image):

- I2C access for IMU (e.g., `smbus2`)
- GPIO access for IR LED PWM

The code is written so these are optional when running on a dev machine.

## Notes

- The current `src/gp2/main.py` passes camera frames into `FatigueDetector`; when MediaPipe is available, real landmarks are extracted.
- For production-like testing of telemetry, prefer a local MQTT broker with authentication and TLS.
