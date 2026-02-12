import json
import time

try:
    import paho.mqtt.client as mqtt  # type: ignore
except ImportError:  # pragma: no cover
    mqtt = None

BROKER = "test.mosquitto.org" # Replace with your Cloud IP
PORT = 1883
TOPIC_TELEMETRY = "smarthelmet/v1/telemetry"
TOPIC_ALERTS = "smarthelmet/v1/alerts"

class TelemetryClient:
    def __init__(self, device_id="helmet_01"):
        if mqtt is None:
            self.client = None
            self.device_id = device_id
            print("MQTT client unavailable (install paho-mqtt to enable telemetry).")
            return

        self.client = mqtt.Client(device_id)
        self.device_id = device_id

        try:
            self.client.connect(BROKER, PORT, 60)
            self.client.loop_start()
        except Exception as e:
            print(f"MQTT Connection Failed: {e}")

    def send_alert(self, alert_type, value):
        if self.client is None:
            return
        payload = {
            "device_id": self.device_id,
            "type": "ALERT",
            "alert": alert_type,
            "value": value,
            "timestamp": time.time()
        }
        self.client.publish(TOPIC_ALERTS, json.dumps(payload), qos=1)

    def send_telemetry(self, perclos, g_force):
        if self.client is None:
            return
        payload = {
            "device_id": self.device_id,
            "type": "STATUS",
            "perclos": perclos,
            "g_force": g_force
        }
        self.client.publish(TOPIC_TELEMETRY, json.dumps(payload), qos=0)