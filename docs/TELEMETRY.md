# Telemetry

Telemetry uses MQTT publish/subscribe semantics.

Implementation: `src/gp2/telemetry.py`.

## Broker and topics

Default settings in the prototype:

- Broker: `test.mosquitto.org`
- Port: `1883`
- Telemetry topic: `smarthelmet/v1/telemetry`
- Alerts topic: `smarthelmet/v1/alerts`

Connectivity is configured via `ConnectivityConfig` (`src/gp2/planning/connectivity.py`) and consumed by `TelemetryClient`.

## Message types

### Status telemetry (qos=0)

Published by `TelemetryClient.send_telemetry(perclos, g_force, sensor_health=None, power_profile=None)`.

Example payload (JSON):

```json
{
  "device_id": "helmet_01",
  "type": "STATUS",
  "perclos": 0.05,
  "g_force": 1.02,
  "sensor_health": {
    "imu": {
      "available": true,
      "mode": "hardware",
      "bus": "I2C",
      "direction": "bidirectional"
    },
    "camera": {
      "available": true,
      "mode": "hardware",
      "bus": "CSI/USB",
      "direction": "camera->board"
    },
    "ir": {
      "available": true,
      "mode": "hardware",
      "bus": "GPIO/PWM",
      "direction": "board->ir"
    }
  },
  "power_profile": {
    "average_ma": 948.0,
    "peak_ma": 1812.0,
    "standby_ma": 269.0,
    "bounds_valid": true
  }
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

Then run `PYTHONPATH=src python -m gp2.main` and observe incoming messages.

## Runtime reliability behavior

- QoS for status and alerts is configurable (`status_qos`, `alert_qos`).
- When connectivity is unavailable, unsent messages can be queued (`offline_queue_enabled`).
- Queue length is bounded by `offline_queue_max_items`.
- Reconnect attempts use exponential backoff and then replay queued payloads on success.

## Security note

The prototype uses a public broker without TLS. For a real deployment:

- Use a private broker
- Enable authentication and TLS
- Consider message signing / integrity protection
