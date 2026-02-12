# Connectivity

This document defines communication between the GP2 device and application/cloud systems.

## Application ↔ Device communication

Primary path (prototype):

- Device publishes telemetry and alerts via MQTT topics.
- Application or backend subscribes and stores/visualizes events.

Optional direct path:

- Bluetooth or USB link for local setup and diagnostics.

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

## Message classes

- STATUS: periodic operational metrics (for example fatigue score, g-force)
- ALERT: discrete high-priority events (CRASH/FATIGUE)
- HEALTH: optional diagnostics (sensor availability, battery state)

## Reliability and quality-of-service strategy

- STATUS messages can use lower QoS and tolerate occasional loss.
- ALERT messages should use acknowledged delivery (for example MQTT QoS 1).
- Offline periods require local queueing and replay on reconnect.

## Security checklist

- [ ] Enforce authentication for publish/subscribe paths
- [ ] Use TLS for transport encryption
- [ ] Rotate device credentials and revoke compromised nodes
- [ ] Limit topic permissions by device identity
