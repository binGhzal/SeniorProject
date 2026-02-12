# TODO 05: Data Storage Strategy

- [x] Define on-device retention window and queue size
- [ ] Define app-side schema for trips, events, and diagnostics
- [ ] Define event-clip metadata schema for circular buffer windows (±10-20s around events)
- [x] Decide cloud storage scope (alerts-only vs full telemetry)
- [x] Define synchronization conflict and replay rules
- [ ] Define encryption and privacy controls for sensitive data
- [ ] Define DSAR-compatible export/delete workflow for user-requested data actions

## Implementation plan

- Week 3: define app schema v1 for trip summaries, event timeline, and diagnostics.
- Week 3: add encryption-at-rest policy and key handling guidance for local event data.
- Week 3: add schema compatibility tests for serialization/deserialization boundaries.
