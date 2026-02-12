# Hardware Architecture

This document maps the GP2 hardware stack, interfaces, and board-level control logic.

## Overall hardware architecture

The prototype target is a smart-helmet node with these blocks:

- Main compute board (edge runtime for sensing + detection + telemetry)
- IMU sensor block (accelerometer for crash detection)
- Camera module (eye landmarks for fatigue analysis)
- IR illumination block (low-light support)
- Power subsystem (battery + regulation)
- Connectivity subsystem (wireless or wired uplink)

## Interfaces between board and sensors/actuators

### Main board ↔ IMU

- Bus: I²C (current prototype assumption)
- Direction: - Board -> IMU: configuration writes - IMU -> Board: sampled acceleration registers

### Main board ↔ Camera

- Bus: CSI/USB (implementation-dependent)
- Direction: - Camera -> Board: video frames - Board -> Camera: control settings (exposure/FPS)

### Main board ↔ IR LEDs

- Bus: GPIO/PWM
- Direction: - Board -> IR driver/LEDs: brightness duty-cycle command

## Communication protocols

- I²C: IMU register reads/writes
- GPIO/PWM: IR brightness control
- CSI/USB: camera transport (platform-specific)
- UART/SPI: reserved for future sensors or modem expansion

## Signal direction and control logic

Control loop summary:

1. Board samples IMU and camera inputs.
2. Detection logic classifies fatigue/crash conditions.
3. Board emits alerts and periodic telemetry.
4. Board adjusts actuators (for example IR brightness) based on conditions.

Implementation note (current prototype):

- Interface metadata is centralized in `src/gp2/planning/hardware_architecture.py`.
- Runtime modules in `src/gp2/sensors.py` consume the same interface specs.
- Health telemetry now includes per-module `bus` and `direction` fields to reflect these shared constants.

## Integration checklist

- [ ] Confirm final IMU part number and register map
- [ ] Confirm camera interface and frame-rate target
- [ ] Confirm IR driver current limits and PWM range
- [ ] Capture final pin map and electrical constraints

## Hardware decision record (to freeze)

Use this section to lock final hardware selections.

| Item       | Selected part/SKU              | Constraint target                         | Status                              |
| ---------- | ------------------------------ | ----------------------------------------- | ----------------------------------- |
| Main board | TBD                            | Linux userspace + camera + MQTT runtime   | Pending physical selection          |
| IMU        | TBD                            | 3-axis accel, I²C, stable register map    | Pending physical selection          |
| Camera     | TBD                            | >=640x480, low-light workable, stable FPS | Pending physical selection          |
| IR driver  | PWM-controlled LED driver path | Safe current-limited LED operation        | Design defined, measurement pending |

## Startup sequence and verification checklist

Reference startup sequence from runtime (`src/gp2/main.py`):

1. Initialize IMU, camera, and IR modules.
2. Validate connectivity configuration and telemetry client setup.
3. Build sensor-health snapshot and power-profile snapshot.
4. Set IR brightness default and enter monitoring loop.

Verification log template:

| Step              | Expected state                             | Observed state | Pass/Fail | Notes |
| ----------------- | ------------------------------------------ | -------------- | --------- | ----- |
| Sensor init       | IMU/camera/IR modules return health status | TBD            | TBD       |       |
| Connectivity init | Config valid and client ready              | TBD            | TBD       |       |
| Health snapshot   | bus/direction fields present               | TBD            | TBD       |       |
| Loop start        | status/alerts emitted as expected          | TBD            | TBD       |       |

Automation hook:

Use `src/gp2/planning/hardware_power_validation.py` (`HardwareEvidence`) to
evaluate whether TODO 02 closeout criteria are satisfied.

## IR subsystem driver and current path

Reference control path:

- Board GPIO/PWM output -> IR driver stage -> IR LED load.
- Runtime duty-cycle control is exposed by `IRSys.set_brightness(...)`.
- Driver implementation must enforce current limits from LED and regulator specs.

Design checks:

- Add current limiting (driver or resistor) for worst-case duty cycle.
- Keep thermal envelope within enclosure limits.
- Verify PWM frequency and duty range do not induce flicker artifacts.

## Pin-map template (final board integration)

| Function      | Signal  | Board pin | Direction       | Voltage rail  | Notes |
| ------------- | ------- | --------- | --------------- | ------------- | ----- |
| IMU I²C clock | SCL     | TBD       | Board -> IMU    | 3.3V          |       |
| IMU I²C data  | SDA     | TBD       | Bidirectional   | 3.3V          |       |
| Camera data   | CSI/USB | TBD       | Camera -> Board | Board-defined |       |
| IR PWM        | PWM_OUT | TBD       | Board -> Driver | 3.3V logic    |       |
| Power input   | VIN     | TBD       | Supply -> Board | 5V nominal    |       |
