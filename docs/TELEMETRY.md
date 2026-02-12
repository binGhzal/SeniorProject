# Telemetry

Telemetry uses MQTT publish/subscribe semantics.

Implementation: `unit-tests/telemetry.py`.

## Broker and topics

Default settings in the prototype:

- Broker: `test.mosquitto.org`
- Port: `1883`
- Telemetry topic: `smarthelmet/v1/telemetry`
- Alerts topic: `smarthelmet/v1/alerts`

## Message types

### Status telemetry (qos=0)

Published by `TelemetryClient.send_telemetry(perclos, g_force)`.

Example payload (JSON):

```json
{
  "device_id": "helmet_01",
  "type": "STATUS",
  "perclos": 0.05,
  "g_force": 1.02
}
```

### Alerts (qos=1)

Published by `TelemetryClient.send_alert(alert_type, value)`.

Example payload (JSON):

```json
{
  "device_id": "helmet_01",
  "type": "ALERT",
  "alert": "CRASH",
  "value": 3.0,
  "timestamp": 1700000000.0
}
```

## How to verify publishes (manual)

Use any MQTT client to subscribe:

- Subscribe to `smarthelmet/v1/telemetry`
- Subscribe to `smarthelmet/v1/alerts`

Then run `unit-tests/main.py` and observe incoming messages.

## Security note

The prototype uses a public broker without TLS. For a real deployment:

- Use a private broker
- Enable authentication and TLS
- Consider message signing / integrity protection
