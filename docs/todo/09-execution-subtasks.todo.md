# TODO 09: Execution Subtasks and Anti-Drift Plan

Purpose: keep implementation aligned with original GP1→GP2 scope by defining concrete subtasks, acceptance checks, and evidence for each TODO file.

Execution rules:

- Complete software-first subtasks in code + tests + docs in one change set.
- Mark hardware/field subtasks as blocked only with explicit evidence notes.
- Do not close a parent TODO item unless acceptance checks and artifacts are linked.

## TODO 01: Feature Definition

### Subtasks

- [ ] T01-1 Freeze app platform decision (`mobile`, `web`, or `both`) in `docs/FEATURES.md`.
- [ ] T01-2 Add 8-12 user stories (pairing, live monitoring, alerts, trip history) with acceptance criteria.
- [ ] T01-3 Add MVP vs post-MVP matrix and map each feature to telemetry/test evidence.
- [ ] T01-4 Add explicit board-side acceptance criteria (crash, fatigue, health, storage).

### Acceptance

- [ ] `docs/FEATURES.md` contains platform, stories, matrix, and traceability links.

## TODO 02: Hardware Architecture

### Subtasks

- [ ] T02-1 Freeze board SKU and compute constraints table in `docs/HARDWARE.md`.
- [ ] T02-2 Freeze IMU/camera part numbers and interface modes.
- [ ] T02-3 Add IR driver/current path description and startup control sequence.
- [ ] T02-4 Add final pin map and signal-direction diagram reference.
- [ ] T02-5 Add measured startup behavior notes from board test run.

### Acceptance

- [ ] `docs/HARDWARE.md` includes frozen parts + pin map references + startup evidence.

## TODO 03: Power Supply Plan

### Subtasks

- [ ] T03-1 Add voltage rails and tolerances table.
- [ ] T03-2 Add measured avg/peak/standby current worksheet (day/night).
- [ ] T03-3 Add battery target and charging strategy rationale.
- [ ] T03-4 Add runtime estimate worksheet and >=8h validation procedure.
- [ ] T03-5 Add brownout/overcurrent protection plan.

### Acceptance

- [ ] `docs/POWER.md` includes measurement-backed tables and explicit protection strategy.

## TODO 04: Connectivity

### Subtasks

- [x] T04-1 Implement reconnect + bounded offline replay behavior.
- [x] T04-2 Add reconnect retry ceiling and fault counters.
- [x] T04-3 Add runtime health snapshot fields (queue depth, degraded mode).
- [ ] T04-4 Freeze primary transport path and backup path policy.
- [ ] T04-5 Freeze topic schema and payload contracts.
- [ ] T04-6 Freeze telemetry cadence and alert latency SLO targets.
- [ ] T04-7 Add TLS/auth/credential rotation deployment policy.

### Acceptance

- [x] Tests validate replay + retry ceiling behavior in `tests/test_runtime.py`.
- [ ] `docs/CONNECTIVITY.md` includes transport + contract + security final decisions.

## TODO 05: Data Storage Strategy

### Subtasks

- [x] T05-1 Implement retention and bounded local queue.
- [x] T05-2 Implement replay/sync hooks and conflict policy.
- [ ] T05-3 Define app schema v1 (`trip_summary`, `event_record`, `diagnostic_record`).
- [ ] T05-4 Define clip metadata schema (±10-20s around triggers).
- [ ] T05-5 Define encryption-at-rest and key handling policy.
- [ ] T05-6 Define DSAR export/delete workflow and API contract.

### Acceptance

- [ ] `docs/STORAGE.md` contains schema v1 + clip metadata + privacy/DSAR policy.
- [ ] Schema compatibility tests exist for serialization boundaries.

## TODO 06: Software Architecture

### Subtasks

- [x] T06-1 Keep single orchestrator cycle contract stable.
- [x] T06-2 Add runtime fault counters and degraded-mode telemetry.
- [x] T06-3 Add reconnect retry-ceiling tests.
- [ ] T06-4 Define watchdog escalation policy and trigger thresholds.

### Acceptance

- [x] Runtime emits `runtime_health` with telemetry and local fault counters.
- [ ] Architecture docs include watchdog escalation table.

## TODO 07: AI and Advanced Algorithms

### Subtasks

- [ ] T07-1 Freeze dataset buckets and labeling taxonomy.
- [ ] T07-2 Add distraction path requirements (gaze/head-pose) and validation protocol.
- [ ] T07-3 Add baseline benchmark template for latency/false-alert results.
- [ ] T07-4 Add rollout acceptance gate table (go/no-go).

### Acceptance

- [ ] `docs/AI.md` includes dataset taxonomy, distraction protocol, and acceptance gates.

## TODO 08: GP1 Carry-Forward Scope

### Subtasks

- [ ] T08-1 Define distraction trigger contract and event payload fields.
- [ ] T08-2 Define circular event-clip buffering workflow contract.
- [ ] T08-3 Define dashboard integration contract for trends/events/clips.
- [ ] T08-4 Define emergency escalation routing policy.
- [ ] T08-5 Define benchmark harness for `<200ms` path and false-alert baseline.
- [ ] T08-6 Define privacy toggles (consent/events-only) and DSAR endpoints.

### Acceptance

- [ ] `docs/todo/08-gp1-carry-forward.todo.md` items are either completed or explicitly moved to post-MVP backlog with rationale.

## Weekly cadence and evidence log

- Week close checklist:
    - [ ] Update parent TODO checkboxes
    - [ ] Update architecture/report docs
    - [ ] Attach test output/benchmark artifact
    - [ ] Record blocked items with reason + next action
