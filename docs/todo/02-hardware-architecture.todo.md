# TODO 02: Hardware Architecture

- [x] Add runtime startup sensor health snapshot wiring (IMU/camera/IR)
- [x] Expose per-module availability/mode status for telemetry
- [x] Share interface constants between planning and runtime modules
- [x] Complete Phase 2 software architecture integration deliverables

- [ ] Confirm board SKU and compute constraints
- [ ] Confirm IMU part and electrical interface details
- [ ] Confirm camera module and interface bandwidth needs
- [ ] Document IR subsystem driver and current path
- [ ] Produce final pin map and interface diagram
- [ ] Verify signal direction and startup control sequence

## Implementation plan

- Week 1: freeze target board SKU + IMU/camera part numbers and update `docs/HARDWARE.md`.
- Week 1: create final pin map + signal-direction diagram and attach to report figures.
- Week 2: run startup sequencing test on target board and record measured initialization behavior.
