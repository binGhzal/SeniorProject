# TODO 08: GP1 Carry-Forward Scope (Deferred to GP2+)

This checklist captures high-value requirements documented in the GP1 report that
remain deferred from the current MVP runtime.

## Functional carry-forward items

- [x] Add distraction detection path (gaze + head-pose indicators) and define trigger policy.
- [x] Add circular event-clip buffering workflow (store ±10-20s around trigger events).
- [x] Define dashboard integration contract for events, clips, and trend metrics.
- [x] Define emergency/escalation routing policy for critical crash events.

## Validation and performance carry-forward items

- [ ] Validate end-to-end alert latency target (`<200ms`) in benchmark environment.
- [ ] Establish false-alert baseline and acceptance gate (target from GP1 planning).
- [ ] Validate day-use power/runtime objective (continuous operation target >= 8 hours).

Deferred note:

- These three validation items are explicitly moved to post-MVP benchmark backlog
  because they require hardware-in-loop measurement runs.

## Privacy and governance carry-forward items

- [x] Implement consent toggles and events-only operation mode for privacy minimization.
- [x] Define retention controls and deletion policy for event clips and summaries.
- [x] Define DSAR workflows (access/export/correction/deletion requests).

## Suggested implementation sequence

- Sprint E1: distraction + clip schema + dashboard event contract.
- Sprint E2: latency/false-alert benchmark harness and baseline results.
- Sprint E3: privacy/DSAR workflow documentation and implementation hooks.

Current implementation notes:

- Contracts and baseline targets are defined in
  `src/gp2/planning/carry_forward.py`.
- Benchmark execution itself remains open and requires measured runs.
