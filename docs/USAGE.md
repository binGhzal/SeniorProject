# Running the Prototype

The prototype orchestration loop is in `src/gp2/main.py`.

## Run on a development machine

1. Install optional runtime deps (recommended):

```bash
python -m pip install numpy paho-mqtt opencv-python
```

1. Run the loop:

```bash
PYTHONPATH=src python -m gp2.main
```

## What you should see

On startup:

- `System Initialized. Starting Monitoring...`

During execution:

- Crash alerts appear in logs with g-force values.
- Fatigue alerts appear in logs with EAR values.

Stop with Ctrl+C.

## Important behaviors (prototype)

- Crash threshold: `total_g > 2.5`
- Fatigue thresholding is handled by `FatigueDetector` using a rolling closed-eye buffer.
- When `mediapipe` + camera input are available, landmarks are extracted from frames in `src/gp2/detection.py`.

## On-device (Raspberry Pi) notes

- Ensure camera permissions and correct device index.
- Ensure I2C is enabled (for IMU).
- Ensure the GPIO pin matches your IR LED driver wiring.

For payload schemas and topics, see `TELEMETRY.md`.
