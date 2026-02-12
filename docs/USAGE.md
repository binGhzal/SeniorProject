# Running the Prototype

The prototype orchestration loop is in `src/gp2/main.py`.

## Run on a development machine

1. Install optional runtime deps (recommended):

```bash
python -m pip install numpy paho-mqtt opencv-python
```

2. Run the loop:

```bash
PYTHONPATH=src python -m gp2.main
```

## What you should see

On startup:

- `System Initialized. Starting Monitoring...`

During execution:

- If a high-g event is detected: `CRASH DETECTED! G-Force: <value>`
- If fatigue is detected: `FATIGUE ALERT! EAR: <value>`

Stop with Ctrl+C.

## Important behaviors (prototype)

- Crash threshold: `total_g > 2.5`
- Fatigue thresholding is handled by `FatigueDetector` using a rolling closed-eye buffer.
- Landmarks in `main.py` are currently simulated as zeros; this means fatigue triggering depends on the detector logic and configured thresholds, not on real camera input.

## On-device (Raspberry Pi) notes

- Ensure camera permissions and correct device index.
- Ensure I2C is enabled (for IMU).
- Ensure the GPIO pin matches your IR LED driver wiring.

For payload schemas and topics, see `TELEMETRY.md`.
