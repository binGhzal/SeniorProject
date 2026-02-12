from dataclasses import dataclass


@dataclass
class ConnectivityConfig:
    protocol: str = "mqtt"
    telemetry_interval_s: float = 1.0
    max_alert_latency_s: float = 2.0
    offline_queue_enabled: bool = False


def validate_connectivity_config(config: ConnectivityConfig) -> bool:
    if config.telemetry_interval_s <= 0:
        return False
    if config.max_alert_latency_s <= 0:
        return False
    return config.protocol.lower() in {"mqtt", "ble", "usb", "wifi"}
