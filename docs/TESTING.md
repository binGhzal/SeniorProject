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

## Testing methods (detailed)

This section documents **how** testing is performed, **why** each method is used,
and how each method reduces a specific project risk.

### Method A: Unit tests with dependency isolation

- **What it is:** verify one module behavior at a time (sensor wrappers,
  detector logic branches, policy helpers).
- **How it is executed:** replace hardware/network boundaries with
  `unittest.mock` objects (I2C bus, MQTT client, detector outputs).
- **Why this method:** hardware and connectivity are variable in CI/dev machines;
  deterministic mocks keep failures attributable to logic changes rather than
  environment conditions.
- **Primary risks mitigated:** regression in payload schema, threshold conditions,
  and policy validation.

### Method B: Integration-style contract-cycle tests

- **What it is:** execute one full runtime cycle through injected boundaries
  (read snapshot -> detect -> publish events).
- **How it is executed:** `RuntimeOrchestratorContract` callbacks are provided by
  test doubles to force known crash/fatigue scenarios and capture emitted events.
- **Why this method:** validates module wiring and event ordering, not only
  isolated function outputs.
- **Primary risks mitigated:** broken orchestration flow, missing event emission,
  and payload handoff mismatches across modules.

### Method C: Policy and resilience tests

- **What it is:** validate offline queue bounds, storage retention pruning,
  conflict-resolution behavior, and QoS routing.
- **How it is executed:** controlled event injection with synthetic timestamps,
  bounded queue sizes, and configurable connectivity options.
- **Why this method:** these paths are safety/availability critical and easy to
  regress during refactors if left as manual checks.
- **Primary risks mitigated:** data loss during disconnects, unbounded growth,
  and incorrect replay semantics.

### Method D: Manual hardware-facing verification

- **What it is:** on-device checks for camera capture, IR brightness control,
  and physical startup behavior.
- **How it is executed:** run the loop on target hardware and verify sensor health,
  IR response, and telemetry outputs under day/night conditions.
- **Why this method:** some behaviors depend on physical peripherals and cannot be
  fully represented by mocks.
- **Primary risks mitigated:** deployment-only failures (driver mismatch,
  unavailable peripherals, wiring assumptions).

## Acceptance criteria and reasoning

Automated tests currently provide high confidence for **correctness of logic and
contracts**. GP1 carry-forward targets add **performance/operational** criteria
that are tracked as TODO work and validated in staged field tests.

| Criterion                                          | Validation method                          | Rationale                                          |
| -------------------------------------------------- | ------------------------------------------ | -------------------------------------------------- |
| Module correctness                                 | Unit tests                                 | Fast regression detection per module               |
| Runtime integration                                | Contract-cycle test                        | Ensures crash/fatigue/status wiring remains intact |
| Offline behavior                                   | Queue/replay and retention tests           | Protects reliability during network interruptions  |
| Alert latency target (`<200ms`, GP1 carry-forward) | Planned benchmark + timestamped event path | Confirms real-time behavior under realistic load   |
| False-alert target (GP1 carry-forward baseline)    | Planned dataset-driven evaluation          | Prevents unsafe alert fatigue and poor trust       |
| 8-hour operational target (GP1 carry-forward)      | Planned power/runtime field profile        | Confirms practical deployment endurance            |

## Reproducibility notes

- Run tests from repository root to preserve import paths.
- Keep optional dependencies optional for logic tests; only enable hardware libs
  for on-device verification.
- Treat benchmark and field-validation scripts as separate evidence from unit
  test success (both are required for final operational claims).

## Coverage map (all components)

- **IMU (`IMUSensor`)**: unit-tested via mocking I2C reads
  (`test_imu_connection`).
- **Fatigue detection (`FatigueDetector`)**: logic-trigger is unit-tested via
  software injection (`test_fatigue_logic`).
- **Crash detection threshold**: integration-style test validates alert trigger
  (`test_crash_integration`).
- **Camera (`CameraModule`)**: not unit-tested; manual verification by running
  the loop and confirming frames are non-`None`.
- **IR LEDs (`IRSys`)**: not unit-tested; manual on-device verification
  (brightness changes).
- **Telemetry (`TelemetryClient`)**: unit-tested for payload shape, QoS routing,
  and offline queue behavior.
- **FaceMesh integration (`src/gp2/detection.py`)**: logic path is covered, but
  accuracy against real video remains manual/experimental.

Current suite scope extends beyond the original three baseline tests and now also
covers connectivity policy, storage retention/replay, runtime contract execution,
power profile validation, and AI metrics fields.

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

```text
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

```text
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

```text
[Pass] Crash Integration (Sensor -> Cloud Trigger) Verified
```

## Expected full output (example)

A successful run should resemble:

```text
test_crash_integration (...)
...
ok

test_fatigue_logic (...)
...
ok

test_imu_connection (...)
...
ok

... additional tests for connectivity, storage, architecture contracts, and AI metrics ...

----------------------------------------------------------------------
Ran <N> tests in <time>s

OK
```

## Notes on dependencies

- **Required for unit tests:** `numpy`
- **Optional:**
    - `paho-mqtt` (telemetry)
    - `opencv-python` (camera on non-Pi machines)
    - Raspberry Pi I/O libraries for I2C/GPIO
