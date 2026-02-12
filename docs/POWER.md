# Power Supply Plan (Electrical Specifications)

This document defines interface voltages, subsystem power demand, and estimated power budget.

## Voltage levels per interface

- Main compute rail: 5V input (typical SBC profile)
- Logic rails: 3.3V digital interfaces (I²C/GPIO)
- Sensor rails: 3.3V (IMU) and camera-specific rail(s)
- Actuator rail: IR illumination rail sized by LED current demand

Design target tolerances (planning baseline):

- 5V rail: ±5%
- 3.3V logic rail: ±5%
- Brownout trigger threshold: board-specific (must be documented per selected SKU)

> Final values must be confirmed against selected board and module datasheets.

## Power requirements by subsystem

### Compute board

- Average: workload-dependent (idle vs active inference)
- Peak: high CPU + wireless transmit + camera capture

### IMU + low-speed sensors

- Typically low-power compared to camera and compute

### Camera module

- Moderate draw, higher during continuous capture

### IR illumination

- Highly duty-cycle dependent; can dominate nighttime power

### Connectivity radio

- Bursty peaks during transmit windows

## Power distribution architecture

Recommended distribution:

1. Battery pack -> protection/charging stage
2. Primary regulator -> board input rail
3. Secondary regulators -> 3.3V and sensor rails
4. Switched rail or PWM control for IR subsystem

Regulator sizing rule of thumb:

- Required regulator max current >= expected peak current \* (1 + margin)
- Default planning margin: 20%
- Helper available in code: `regulator_margin_ok(...)`

## Power budget estimation template

Use this table and replace placeholders with measured values.

| Subsystem          | Average (mA) | Peak (mA) | Standby (mA) | Notes                    |
| ------------------ | -----------: | --------: | -----------: | ------------------------ |
| Compute board      |          TBD |       TBD |          TBD | Model-dependent          |
| IMU                |          TBD |       TBD |          TBD | Sampling-rate dependent  |
| Camera             |          TBD |       TBD |          TBD | FPS/resolution dependent |
| IR system          |          TBD |       TBD |          TBD | Duty-cycle dependent     |
| Radio/Connectivity |          TBD |       TBD |          TBD | Protocol dependent       |
| **Total**          |      **TBD** |   **TBD** |      **TBD** |                          |

## Runtime implementation status

Current runtime implementation includes a software power-profile model in `src/gp2/planning/power_plan.py`:

- `PowerProfile` data model for average, peak, and standby current estimates.
- `estimate_total_current(...)` to aggregate subsystem estimates.
- `has_valid_power_bounds(...)` to verify `peak >= average >= standby >= 0`.
- `estimate_runtime_hours(...)` to estimate runtime from battery/load assumptions.
- `required_battery_capacity_mah(...)` to size battery for target runtime.
- `meets_runtime_target(...)` to evaluate `>= 8h` runtime objective.
- `regulator_margin_ok(...)` to validate regulator headroom against peak load.

The runtime loop (`src/gp2/main.py`) builds a `power_profile` snapshot and
includes it in STATUS telemetry payloads when telemetry is enabled.

## Validation checklist

- [ ] Measure current in active mode
- [ ] Measure current in standby mode
- [ ] Measure peak current during alert + publish burst
- [ ] Estimate battery runtime for representative duty cycle

## Runtime estimation worksheet

Use measured or assumed values:

- Battery capacity (mAh):
- Average current (mA):
- Derating factor (0-1):
- Estimated runtime hours = `(capacity * derating) / average_current`

Day/night profile template:

| Profile           | Avg current (mA) | Estimated runtime (h) | Meets >=8h? |
| ----------------- | ---------------: | --------------------: | ----------- |
| Day               |              TBD |                   TBD | TBD         |
| Night (IR active) |              TBD |                   TBD | TBD         |

Automation hook:

- Use `src/gp2/planning/hardware_power_validation.py` (`PowerEvidence`) to
  evaluate TODO 03 closeout readiness against runtime and protection criteria.

## Protection strategy baseline

- Brownout handling: define threshold and safe shutdown/degraded mode behavior.
- Overcurrent handling: include fuse/current-limit stage in supply path.
- Thermal margin: validate regulator and board temperatures under peak load.
