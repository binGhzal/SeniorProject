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

- [ ] Local database: (SQLite / IndexedDB / local files)
- [ ] Data model: (trips, events, samples)
- [ ] Export: CSV/JSON for reports

## Cloud storage (if applicable)

- [ ] Cloud provider/service: (TBD)
- [ ] Data uploaded: alerts only vs full telemetry
- [ ] Access model: user account + device ownership

## Data synchronization and security

- [ ] Encryption at rest (on device, in app, in cloud)
- [ ] Encryption in transit (TLS)
- [ ] Data minimization (store only what is needed)
- [ ] Consent and privacy (who can see crash/fatigue data)

Implemented sync/replay hooks:

- `pending_replay_events()` returns unsynced records in insertion order.
- `mark_synced(...)` marks replayed records as synced.
- `resolve_sync_conflict(...)` supports `local-wins`, `remote-wins`, and `last-write-wins` policy.

## Open questions

- [ ] Do we store camera frames? (default should be **no** unless justified)
- [ ] How long do we retain crash events?
