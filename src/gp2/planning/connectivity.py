"""Connectivity configuration models and validation helpers."""

from dataclasses import dataclass

SUPPORTED_PROTOCOLS = {"mqtt", "ble", "usb", "wifi", "cellular"}
PRIMARY_TRANSPORT = "wifi"
BACKUP_TRANSPORT = "usb"


@dataclass(frozen=True)
class TopicContract:
    """Defines topic name, schema version, and payload class."""

    topic: str
    schema_version: str
    payload_class: str


@dataclass(frozen=True)
class ConnectivitySLO:
    """Defines cadence and latency SLO guidance for runtime publishing."""

    status_interval_s: float
    alert_latency_target_s: float
    alert_path_budget_ms: int


@dataclass(frozen=True)
class SecurityPolicy:
    """Defines transport security policy and credential rotation controls."""

    tls_required: bool
    auth_required: bool
    credential_rotation_days: int
    topic_acl_required: bool


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
    security_profile: str = "dev-public-broker"


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


def topic_contracts() -> dict[str, TopicContract]:
    """Return canonical topic contracts for STATUS/ALERT/HEALTH payloads."""

    return {
        "STATUS": TopicContract(
            topic="smarthelmet/v1/telemetry",
            schema_version="v1",
            payload_class="StatusPayload",
        ),
        "ALERT": TopicContract(
            topic="smarthelmet/v1/alerts",
            schema_version="v1",
            payload_class="AlertPayload",
        ),
        "HEALTH": TopicContract(
            topic="smarthelmet/v1/health",
            schema_version="v1",
            payload_class="HealthPayload",
        ),
    }


def default_connectivity_slo() -> ConnectivitySLO:
    """Return default cadence/latency service-level targets."""

    return ConnectivitySLO(
        status_interval_s=1.0,
        alert_latency_target_s=2.0,
        alert_path_budget_ms=200,
    )


def default_security_policy() -> SecurityPolicy:
    """Return baseline security policy for production-oriented deployments."""

    return SecurityPolicy(
        tls_required=True,
        auth_required=True,
        credential_rotation_days=90,
        topic_acl_required=True,
    )


def transport_profile() -> dict[str, str]:
    """Return selected primary and backup transport paths."""

    return {
        "primary": PRIMARY_TRANSPORT,
        "backup": BACKUP_TRANSPORT,
    }
