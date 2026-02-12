# Connectivity

This document defines communication between the GP2 device and application/cloud systems.

## Application ↔ Device communication

Primary path (frozen for MVP):

- Device publishes telemetry and alerts via MQTT topics.
- Application or backend subscribes and stores/visualizes events.

Fallback path:

- Bluetooth or USB link for local setup and diagnostics.

Selected transport profile:

- Primary: Wi-Fi + MQTT transport
- Backup: USB diagnostics path

## Protocol options

- MQTT over TCP/TLS for telemetry/event exchange
- Wi-Fi for internet transport (prototype-friendly)
- Bluetooth LE for provisioning or short-range sync
- USB serial for factory testing and maintenance
- Cellular as future option where Wi-Fi is unavailable

## Data exchange frequency and latency targets

Baseline targets (to be validated):

- Status telemetry cadence: every 0.5 to 2 seconds
- Alert publication: immediate event-driven publish
- End-to-end alert latency target: < 2 seconds on stable network

Frozen runtime SLO defaults:

- Status cadence target: `1.0s`
- Alert publish SLO target: `<=2.0s`
- Alert path budget target (benchmark): `<200ms`

## Message classes

- STATUS: periodic operational metrics (for example fatigue score, g-force)
- ALERT: discrete high-priority events (CRASH/FATIGUE)
- HEALTH: optional diagnostics (sensor availability, battery state)

Topic and payload contracts (v1):

- `smarthelmet/v1/telemetry` → `StatusPayload`
- `smarthelmet/v1/alerts` → `AlertPayload`
- `smarthelmet/v1/health` → `HealthPayload`

## Reliability and quality-of-service strategy

- STATUS messages can use lower QoS and tolerate occasional loss.
- ALERT messages should use acknowledged delivery (for example MQTT QoS 1).
- Offline periods require local queueing and replay on reconnect.

Current runtime implementation status:

- Connectivity configuration is centralized in `src/gp2/planning/connectivity.py` (`ConnectivityConfig`).
- `TelemetryClient` validates connectivity config at startup and consumes configured `status_qos` and `alert_qos`.
- Offline queue placeholders are implemented with bounded queue size (`offline_queue_max_items`).
- Reconnect behavior uses exponential backoff (`reconnect_initial_delay_s` -> `reconnect_max_delay_s`).
- Reconnect attempts are capped by `max_reconnect_attempts` to avoid unbounded retry loops.
- Queued messages are automatically replayed after successful publish/reconnect events.
- Transport health includes queue depth and reconnect/replay fault counters for diagnostics.
- Runtime heartbeat cadence is driven by `telemetry_interval_s` in `src/gp2/main.py`.

## Security checklist

- [x] Enforce authentication for publish/subscribe paths (policy defined)
- [x] Use TLS for transport encryption (policy required)
- [x] Rotate device credentials and revoke compromised nodes (90-day policy)
- [x] Limit topic permissions by device identity (topic ACL policy)

Security policy baseline:

- Require TLS and authenticated device publish/subscription.
- Rotate credentials every 90 days (or immediately on compromise).
- Restrict topic access by device identity and role-specific ACLs.
