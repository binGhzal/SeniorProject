# TODO 08: GP1 Carry-Forward Scope (Deferred to GP2+)

This checklist captures high-value requirements documented in the GP1 report that
remain deferred from the current MVP runtime.

## Functional carry-forward items

- [ ] Add distraction detection path (gaze + head-pose indicators) and define trigger policy.
- [ ] Add circular event-clip buffering workflow (store ±10-20s around trigger events).
- [ ] Define dashboard integration contract for events, clips, and trend metrics.
- [ ] Define emergency/escalation routing policy for critical crash events.

## Validation and performance carry-forward items

- [ ] Validate end-to-end alert latency target (`<200ms`) in benchmark environment.
- [ ] Establish false-alert baseline and acceptance gate (target from GP1 planning).
- [ ] Validate day-use power/runtime objective (continuous operation target >= 8 hours).

## Privacy and governance carry-forward items

- [ ] Implement consent toggles and events-only operation mode for privacy minimization.
- [ ] Define retention controls and deletion policy for event clips and summaries.
- [ ] Define DSAR workflows (access/export/correction/deletion requests).

## Suggested implementation sequence

- Sprint E1: distraction + clip schema + dashboard event contract.
- Sprint E2: latency/false-alert benchmark harness and baseline results.
- Sprint E3: privacy/DSAR workflow documentation and implementation hooks.
