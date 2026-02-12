# Data Storage Strategy

This document defines where GP2 data is stored, for how long, and how it is synchronized securely.

Status: placeholder; current prototype sends telemetry/alerts without persistence.

## On-device storage

- [ ] Storage medium: (flash / SD / none)
- [ ] What is stored:
  - [ ] Recent alerts
  - [ ] Recent telemetry samples / summaries
  - [ ] Crash event snapshot (pre/post window)
- [ ] Retention policy: (e.g., last N hours or N events)

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

## Open questions

- [ ] Do we store camera frames? (default should be **no** unless justified)
- [ ] How long do we retain crash events?
