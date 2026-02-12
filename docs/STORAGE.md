# Data Storage Strategy

This document defines where GP2 data is stored, for how long, and how it is synchronized securely.

Status: partially implemented in software via SQLite-backed local buffer hooks.

## On-device storage

- [ ] Storage medium: (flash / SD / none)
- [ ] What is stored:
    - [ ] Recent alerts
    - [ ] Recent telemetry samples / summaries
    - [ ] Crash event snapshot (pre/post window)
- [ ] Retention policy: (e.g., last N hours or N events)

Current runtime implementation:

- `src/gp2/planning/storage_strategy.py` defines:
    - `StoragePolicy` (retention window, queue bounds, cloud sync flag, conflict policy)
    - `StorageEvent` schema (`event_type`, `payload`, `timestamp`, `synced`)
    - `LocalStorageBuffer` with retention pruning and bounded queue behavior
- Local buffering is currently SQLite-backed (`:memory:` by default in runtime tests/dev);
  file-backed persistence path selection remains a deployment task.
- `src/gp2/main.py` now records:
    - crash alerts
    - fatigue alerts
    - periodic status snapshots
- Retention is enforced by hours (`on_device_retention_hours`) and maximum queue size (`on_device_queue_max_items`).

## Application-side storage

- [x] Local database: SQLite-backed hooks in runtime and app-schema contracts
- [x] Data model: schema v1 contracts for trips, events, diagnostics, and clip metadata
- [ ] Export: CSV/JSON for reports

App schema v1 contracts (see `src/gp2/planning/storage_strategy.py`):

- `TripSummary`: trip window and aggregate event counts
- `StorageEvent`: canonical event timeline payload
- `DiagnosticRecord`: sensor/runtime-health diagnostics snapshot
- `EventClipMetadata`: ±10-20s trigger-centered clip metadata

## Cloud storage (if applicable)

- [ ] Cloud provider/service: (TBD)
- [ ] Data uploaded: alerts only vs full telemetry
- [ ] Access model: user account + device ownership

## Data synchronization and security

- [x] Encryption at rest (policy defined; implementation target documented)
- [x] Encryption in transit (TLS policy defined)
- [x] Data minimization (alerts/status summaries as default storage scope)
- [x] Consent and privacy (events-only and DSAR policy hooks documented)

Implemented sync/replay hooks:

- `pending_replay_events()` returns unsynced records in insertion order.
- `mark_synced(...)` marks replayed records as synced.
- `resolve_sync_conflict(...)` supports `local-wins`, `remote-wins`, and `last-write-wins` policy.

DSAR workflow hooks:

- Supported request actions: `access-export`, `correction`, `delete`
- Policy intent: fulfill account-scoped data requests without exposing unrelated user/device records

## Open questions

- [ ] Do we store camera frames? (default should be **no** unless justified)
- [ ] How long do we retain crash events?
