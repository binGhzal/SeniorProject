# TODO 10: Hardware and Power Evidence Template

Use this template during bench validation to close remaining hardware/power TODOs.

## Session metadata

- Date:
- Engineer:
- Board SKU:
- IMU part:
- Camera module:
- Firmware/runtime commit:

## Hardware verification log

| Check               | Expected                                 | Observed | Pass/Fail | Evidence        |
| ------------------- | ---------------------------------------- | -------- | --------- | --------------- |
| Board boot sequence | Runtime starts without sensor init crash | TBD      | TBD       | photo/log       |
| IMU register read   | Stable XYZ read stream                   | TBD      | TBD       | log             |
| Camera stream       | Stable frame capture at target FPS       | TBD      | TBD       | log             |
| IR PWM path         | Duty-cycle changes brightness level      | TBD      | TBD       | video/log       |
| Pin map continuity  | Signals match selected pinout            | TBD      | TBD       | schematic notes |

## Current measurement log

| Profile | Compute (mA) | IMU (mA) | Camera (mA) | IR (mA) | Radio (mA) | Total avg (mA) | Total peak (mA) |
| ------- | -----------: | -------: | ----------: | ------: | ---------: | -------------: | --------------: |
| Day     |          TBD |      TBD |         TBD |     TBD |        TBD |            TBD |             TBD |
| Night   |          TBD |      TBD |         TBD |     TBD |        TBD |            TBD |             TBD |

## Runtime and target checks

- Battery capacity (mAh):
- Derating factor:
- Estimated runtime day (h):
- Estimated runtime night (h):
- Meets >=8h target (day):
- Meets >=8h target (night):

## Protection and thermal checks

- Brownout threshold configured:
- Overcurrent protection method:
- Regulator max current:
- Peak current headroom >=20%:
- Thermal observation at peak load:

## Closeout mapping to TODOs

- TODO 02 (hardware architecture): - [ ] board SKU confirmed - [ ] IMU/camera details confirmed - [ ] pin map finalized - [ ] startup sequence verified
- TODO 03 (power plan): - [ ] subsystem currents measured - [ ] runtime objective validated - [ ] protection strategy verified
