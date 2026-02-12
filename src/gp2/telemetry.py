"""MQTT telemetry client for GP2 status and alert publishing."""

import json
import time

from .planning.connectivity import ConnectivityConfig, validate_connectivity_config

try:
    import paho.mqtt.client as mqtt  # type: ignore
except ImportError:  # pragma: no cover
    mqtt = None

TOPIC_TELEMETRY = "smarthelmet/v1/telemetry"
TOPIC_ALERTS = "smarthelmet/v1/alerts"


class TelemetryClient:
    """Handles MQTT connectivity and message publishing for runtime events."""

    def __init__(self, device_id="helmet_01", config=None):
        self.config = config or ConnectivityConfig()
        if not validate_connectivity_config(self.config):
            raise ValueError("Invalid connectivity configuration.")

        self.offline_queue = []
        self.client = None
        self.device_id = device_id
        self.fault_counters = {
            "publish_failures": 0,
            "reconnect_attempts": 0,
            "reconnect_failures": 0,
            "replay_attempts": 0,
            "replay_failures": 0,
        }

        if mqtt is None:
            print("MQTT client unavailable (install paho-mqtt to enable telemetry).")
            return

        self.client = mqtt.Client(device_id)
        self._connect_and_start_loop()

    def _connect_and_start_loop(self):
        """Establish initial MQTT connectivity and start client loop."""
        if self.client is None:
            return False

        try:
            self.client.connect(self.config.broker, self.config.port, 60)
            self.client.loop_start()
            self._flush_offline_queue()
            return True
        except (OSError, ConnectionError, ValueError) as e:
            print(f"MQTT Connection Failed: {e}")
            return False

    def _enqueue_offline(self, topic, payload, qos):
        """Queue message payloads while client is unavailable."""
        if not self.config.offline_queue_enabled:
            return

        self.offline_queue.append({"topic": topic, "payload": payload, "qos": qos})
        while len(self.offline_queue) > self.config.offline_queue_max_items:
            self.offline_queue.pop(0)

    def _flush_offline_queue(self):
        """Attempt to replay queued messages when connectivity is available."""
        if self.client is None or not self.offline_queue:
            return {"replayed": 0, "remaining": len(self.offline_queue)}

        remaining = []
        replayed = 0
        for item in self.offline_queue:
            self.fault_counters["replay_attempts"] += 1
            try:
                self.client.publish(item["topic"], json.dumps(item["payload"]), qos=item["qos"])
                replayed += 1
            except (OSError, ConnectionError, ValueError):
                remaining.append(item)
                self.fault_counters["replay_failures"] += 1
        self.offline_queue = remaining
        return {"replayed": replayed, "remaining": len(self.offline_queue)}

    def replay_offline_queue(self):
        """Public wrapper to replay queued messages after connectivity recovery."""
        return self._flush_offline_queue()

    def _attempt_reconnect(self):
        """Reconnect with exponential backoff to restore publish channel."""
        if self.client is None:
            return False

        delay = self.config.reconnect_initial_delay_s
        attempts = 0
        while (
            delay <= self.config.reconnect_max_delay_s
            and attempts < self.config.max_reconnect_attempts
        ):
            attempts += 1
            self.fault_counters["reconnect_attempts"] += 1
            try:
                self.client.reconnect()
                self._flush_offline_queue()
                return True
            except (OSError, ConnectionError, ValueError):
                self.fault_counters["reconnect_failures"] += 1
                time.sleep(delay)
                delay *= 2
        return False

    def recover_connectivity(self):
        """Public wrapper for reconnect/recovery flow with bounded retries."""
        return self._attempt_reconnect()

    def _publish(self, topic, payload, qos):
        """Publish payload with offline queue + reconnect fallback policy."""
        if self.client is None:
            self._enqueue_offline(topic, payload, qos)
            return False

        try:
            self.client.publish(topic, json.dumps(payload), qos=qos)
            if self.offline_queue:
                self._flush_offline_queue()
            return True
        except (OSError, ConnectionError, ValueError):
            self.fault_counters["publish_failures"] += 1
            self._enqueue_offline(topic, payload, qos)
            self._attempt_reconnect()
            return False

    def health_snapshot(self):
        """Return transport health and recovery counters for status telemetry."""
        queue_max = max(1, self.config.offline_queue_max_items)
        queue_ratio = len(self.offline_queue) / queue_max
        return {
            "connected": self.client is not None,
            "offline_queue_depth": len(self.offline_queue),
            "offline_queue_max_items": queue_max,
            "degraded_mode": queue_ratio >= 0.8 or self.fault_counters["reconnect_failures"] > 0,
            "fault_counters": dict(self.fault_counters),
        }

    def send_alert(self, alert_type, value):
        """Publish a high-priority alert event payload."""
        payload = {
            "device_id": self.device_id,
            "type": "ALERT",
            "alert": alert_type,
            "value": value,
            "timestamp": time.time(),
        }
        self._publish(TOPIC_ALERTS, payload, self.config.alert_qos)

    def send_telemetry(
        self,
        perclos,
        g_force,
        sensor_health=None,
        power_profile=None,
        ai_metrics=None,
        runtime_health=None,
    ):
        """Publish periodic status telemetry with optional sensor health metadata."""
        payload = {
            "device_id": self.device_id,
            "type": "STATUS",
            "perclos": perclos,
            "g_force": g_force,
        }
        if sensor_health is not None:
            payload["sensor_health"] = sensor_health
        if power_profile is not None:
            payload["power_profile"] = power_profile
        if ai_metrics is not None:
            payload["ai_metrics"] = ai_metrics
        if runtime_health is not None:
            payload["runtime_health"] = runtime_health
        self._publish(TOPIC_TELEMETRY, payload, self.config.status_qos)
