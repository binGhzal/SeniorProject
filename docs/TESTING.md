# Testing

This project uses Python `unittest`.

## How to run

From the repository root:

```bash
python -m unittest tests/test_runtime.py -v
```

If `numpy` is missing:

```bash
python -m pip install numpy
```

If you are using the repo virtual environment explicitly:

```bash
./.venv/bin/python -m unittest tests/test_runtime.py -v
```

## Coverage map (all components)

- **IMU (`IMUSensor`)**: unit-tested via mocking I2C reads (`test_imu_connection`).
- **Fatigue detection (`FatigueDetector`)**: logic-trigger is unit-tested via software injection (`test_fatigue_logic`).
- **Crash detection threshold**: integration-style test validates alert trigger (`test_crash_integration`).
- **Camera (`CameraModule`)**: not unit-tested; manual verification by running the loop and confirming frames are non-`None`.
- **IR LEDs (`IRSys`)**: not unit-tested; manual on-device verification (brightness changes).
- **Telemetry (`TelemetryClient`)**: not unit-tested; manual verification by subscribing to MQTT topics and observing publishes.
- **FaceMesh snippet (`perclos.py`)**: not tested.

## Test-by-test detail

### 1) IMU sensor wrapper (`IMUSensor`)

**Test:** `TestSmartHelmet.test_imu_connection`

- **Component under test:** `IMUSensor.read_accel()`
- **What it validates:**
  - Returns a 3-tuple `(ax, ay, az)`
  - Can be exercised on a dev machine by mocking the bus read
- **How it is tested:**
  - Replaces `imu.bus.read_i2c_block_data` with a `MagicMock` returning 6 bytes
  - Asserts the return type and length

**Expected output fragment:**

```
[Pass] IMU Data Format Verified
```

### 2) Fatigue detection logic (`FatigueDetector`)

**Test:** `TestSmartHelmet.test_fatigue_logic`

- **Component under test:** `FatigueDetector.analyze_frame()`
- **What it validates:**
  - The “drowsy” condition is triggered when EAR is below threshold
- **How it is tested:**
  - Injects a mocked return `(True, 0.15)` and asserts:
    - `is_drowsy == True`
    - `ear < 0.25`

**Expected output fragment:**

```
[Pass] Fatigue Logic Triggered Correctly
```

### 3) Crash detection integration (sensor → alert trigger)

**Test:** `TestSmartHelmet.test_crash_integration`

- **Component under test:** crash threshold logic used in the runtime loop
- **What it validates:**
  - If `total_g > 2.5`, `send_alert("CRASH", total_g)` is invoked
- **How it is tested:**
  - Mocks IMU to return `(0, 0, 3.0)`
  - Computes `total_g`
  - Asserts `mock_mqtt.send_alert` was called with the expected args

**Expected output fragment:**

```
[Pass] Crash Integration (Sensor -> Cloud Trigger) Verified
```

## Expected full output (example)

A successful run should resemble:

```
test_crash_integration (tests.TestSmartHelmet.test_crash_integration)
Test 4: The 'Shake to Upload' Crash Logic ...
[Pass] Crash Integration (Sensor -> Cloud Trigger) Verified
ok

test_fatigue_logic (tests.TestSmartHelmet.test_fatigue_logic)
Test 5: Fatigue Logic Simulation (Software Injection) ...
[Pass] Fatigue Logic Triggered Correctly
ok

test_imu_connection (tests.TestSmartHelmet.test_imu_connection)
Test 1: Verify IMU reads data format correctly ...
[Pass] IMU Data Format Verified
ok

----------------------------------------------------------------------
Ran 3 tests in <time>s

OK
```

## Notes on dependencies

- **Required for unit tests:** `numpy`
- **Optional:**
  - `paho-mqtt` (telemetry)
  - `opencv-python` (camera on non-Pi machines)
  - Raspberry Pi I/O libraries for I2C/GPIO
