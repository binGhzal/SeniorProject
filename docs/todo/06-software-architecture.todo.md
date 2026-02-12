# TODO 06: Software Architecture

- [x] Freeze module boundaries for sensors/detection/connectivity
- [x] Document runtime model (threads/processes/event loop)
- [x] Confirm libraries and dependency versions
- [x] Define API contracts between board code and app/backend
- [x] Add health monitoring and fault-recovery strategy

## Implementation plan

- Week 2: define watchdog and degraded-mode behavior for sensor/camera/telemetry failures.
- Week 2: add fault counters and recovery telemetry fields to runtime status payload.
- Week 2: add tests for retry ceilings and fallback behavior under repeated faults.
