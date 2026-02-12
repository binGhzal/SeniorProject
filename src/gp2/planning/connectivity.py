"""Connectivity configuration models and validation helpers."""

from dataclasses import dataclass

SUPPORTED_PROTOCOLS = {"mqtt", "ble", "usb", "wifi", "cellular"}


@dataclass
class ConnectivityConfig:
    """Connectivity runtime configuration for telemetry and alerts."""

    protocol: str = "mqtt"
    broker: str = "test.mosquitto.org"
    port: int = 1883
    telemetry_interval_s: float = 1.0
    max_alert_latency_s: float = 2.0
    status_qos: int = 0
    alert_qos: int = 1
    offline_queue_enabled: bool = False
    offline_queue_max_items: int = 100
    reconnect_initial_delay_s: float = 0.5
    reconnect_max_delay_s: float = 8.0
    max_reconnect_attempts: int = 5


def validate_connectivity_config(config: ConnectivityConfig) -> bool:
    """Validate connectivity settings and transport constraints."""

    if config.telemetry_interval_s <= 0:
        return False
    if config.max_alert_latency_s <= 0:
        return False
    if config.port <= 0:
        return False
    if config.status_qos not in {0, 1}:
        return False
    if config.alert_qos not in {0, 1}:
        return False
    if config.reconnect_initial_delay_s <= 0 or config.reconnect_max_delay_s <= 0:
        return False
    if config.reconnect_initial_delay_s > config.reconnect_max_delay_s:
        return False
    if config.max_reconnect_attempts <= 0:
        return False
    if config.offline_queue_max_items <= 0:
        return False
    return config.protocol.lower() in SUPPORTED_PROTOCOLS
