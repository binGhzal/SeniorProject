# GP2 Implementation Roadmap

This roadmap converts `docs/tasks.md` into implementation phases and maps each section to concrete code touchpoints.

## Phase 0: Baseline and guardrails

- Confirm environment and test baseline with `python -m unittest -v` in `unit-tests/`.
- Keep runtime behavior stable while replacing placeholder logic incrementally.
- Treat docs and checklist updates as part of done criteria for every phase.

## Phase 1: Feature Definition to runnable behavior

### Phase 1 scope

- Finalize MVP application features and onboard feature priorities.

### Phase 1 primary docs

- `docs/FEATURES.md`
- `docs/todo/01-feature-definition.todo.md`

### Phase 1 code touchpoints

- `unit-tests/placeholders/features.py`
- `unit-tests/main.py`
- `unit-tests/tests.py`

### Phase 1 deliverables

- Convert feature booleans into a single runtime feature configuration.
- Add tests for enabled/disabled behavior of non-critical features.
- Freeze a minimal feature matrix (MVP vs post-MVP).

## Phase 2: Hardware Architecture integration

### Phase 2 scope

- Translate hardware interface assumptions into explicit initialization and health checks.

### Phase 2 primary docs

- `docs/HARDWARE.md`
- `docs/todo/02-hardware-architecture.todo.md`

### Phase 2 code touchpoints

- `unit-tests/placeholders/hardware_architecture.py`
- `unit-tests/sensors.py`
- `unit-tests/main.py`

### Phase 2 deliverables

- Add interface specification constants shared by sensors and orchestration.
- Add startup validation for IMU, camera, and IR subsystems.
- Add clear runtime health telemetry fields for each sensor block.

## Phase 3: Power Supply plan to measurable telemetry

### Phase 3 scope

- Turn power assumptions into measurable profiles and runtime estimates.

### Phase 3 primary docs

- `docs/POWER.md`
- `docs/todo/03-power-supply.todo.md`

### Phase 3 code touchpoints

- `unit-tests/placeholders/power_plan.py`
- `unit-tests/telemetry.py`
- `unit-tests/tests.py`

### Phase 3 deliverables

- Add a power profile model for average/peak/standby estimates.
- Include optional power metrics in status payloads.
- Add validation tests for budget aggregation and bounds.

## Phase 4: Connectivity hardening

### Phase 4 scope

- Improve transport reliability, configuration, and alert latency handling.

### Phase 4 primary docs

- `docs/CONNECTIVITY.md`
- `docs/todo/04-connectivity.todo.md`

### Phase 4 code touchpoints

- `unit-tests/placeholders/connectivity.py`
- `unit-tests/telemetry.py`
- `unit-tests/main.py`

### Phase 4 deliverables

- Introduce validated connectivity config consumed by telemetry client.
- Add reconnect/backoff and offline queue placeholders.
- Distinguish QoS behavior for status vs alert flows.

## Phase 5: Data Storage strategy implementation

### Phase 5 scope

- Add local persistence contract and retention controls.

### Phase 5 primary docs

- `docs/STORAGE.md`
- `docs/todo/05-data-storage.todo.md`

### Phase 5 code touchpoints

- `unit-tests/placeholders/storage_strategy.py`
- `unit-tests/main.py`
- `unit-tests/tests.py`

### Phase 5 deliverables

- Define local storage interface for events and summaries.
- Add retention policy enforcement hooks.
- Add tests for retention and replay behavior.

## Phase 6: Software Architecture consolidation

### Phase 6 scope

- Stabilize module boundaries and runtime execution model.

### Phase 6 primary docs

- `docs/SOFTWARE_ARCHITECTURE.md`
- `docs/todo/06-software-architecture.todo.md`

### Phase 6 code touchpoints

- `unit-tests/placeholders/software_architecture.py`
- `unit-tests/main.py`
- `unit-tests/sensors.py`
- `unit-tests/detection.py`
- `unit-tests/telemetry.py`

### Phase 6 deliverables

- Define a single orchestrator contract for sensor-read, detect, publish.
- Isolate side effects to boundaries (I/O modules).
- Ensure unit tests cover module contracts, not only happy paths.

## Phase 7: AI and Advanced Algorithms maturation

### Phase 7 scope

- Evolve from fixed heuristics to measurable model strategy.

### Phase 7 primary docs

- `docs/AI.md`
- `docs/todo/07-ai-advanced-algorithms.todo.md`

### Phase 7 code touchpoints

- `unit-tests/placeholders/ai_algorithms.py`
- `perclos.py`
- `unit-tests/detection.py`
- `unit-tests/tests.py`

### Phase 7 deliverables

- Add algorithm mode selection: heuristic vs model-based pipeline.
- Define dataset and evaluation hooks without breaking runtime loop.
- Add latency and false-alert tracking fields for validation.

## Definition of done per phase

- Checklist section items updated in matching file under `docs/todo/`.
- Corresponding architecture/section doc updated with final decisions.
- Unit tests added or updated for new behavior.
- Existing test suite remains green.

## Suggested execution order and cadence

- Implement phases 1 through 4 first for a stable operational core.
- Implement phases 5 through 7 after connectivity and reliability are stable.
- Use small pull requests, each mapped to one phase and one checklist file.
