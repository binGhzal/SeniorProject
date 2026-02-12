# TODO 03: Power Supply Plan

- [x] Add runtime power-profile model (average/peak/standby)
- [x] Add power bounds validation logic and tests
- [x] Include `power_profile` in STATUS telemetry payloads
- [x] Complete Phase 3 software deliverables

- [x] Confirm required voltage rails and tolerances
- [ ] Measure subsystem current draw (avg/peak/standby)
- [x] Size regulators and thermal margins
- [x] Define battery capacity target and charging strategy
- [x] Estimate runtime for day/night operating profiles
- [ ] Validate continuous operation target (>= 8 hours) under representative duty cycle
- [x] Add brownout and overcurrent protection plan

## Implementation plan

- Week 2: measure average/peak current for compute, camera, IR, and radio under day/night scenarios.
- Week 3: finalize battery and charging design targets with thermal margin calculations.
- Week 3: document protection strategy (brownout, overcurrent) and link to hardware diagram.

## Blockers and next evidence required

- Current-draw measurements require instrumented hardware test setup.
- 8-hour validation requires representative duty-cycle bench runs on final board.
