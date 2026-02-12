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
- Direction:
  - Board -> IMU: configuration writes
  - IMU -> Board: sampled acceleration registers

### Main board ↔ Camera

- Bus: CSI/USB (implementation-dependent)
- Direction:
  - Camera -> Board: video frames
  - Board -> Camera: control settings (exposure/FPS)

### Main board ↔ IR LEDs

- Bus: GPIO/PWM
- Direction:
  - Board -> IR driver/LEDs: brightness duty-cycle command

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

## Integration checklist

- [ ] Confirm final IMU part number and register map
- [ ] Confirm camera interface and frame-rate target
- [ ] Confirm IR driver current limits and PWM range
- [ ] Capture final pin map and electrical constraints
