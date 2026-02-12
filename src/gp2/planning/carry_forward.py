"""GP1 carry-forward planning contracts for deferred GP2+ features."""

from dataclasses import dataclass


@dataclass(frozen=True)
class DistractionTriggerContract:
    """Contract for distraction event trigger payloads."""

    event_type: str = "DISTRACTION"
    required_signals: tuple[str, ...] = ("gaze_offset", "head_pitch", "head_yaw")
    trigger_window_s: float = 2.0


@dataclass(frozen=True)
class ClipBufferContract:
    """Contract for circular event-clip buffering metadata."""

    pre_event_s: int = 10
    post_event_s: int = 20
    storage_mode: str = "ring-buffer"
    redact_faces_by_default: bool = True


@dataclass(frozen=True)
class DashboardIntegrationContract:
    """Contract for dashboard ingestion of event and trend records."""

    endpoint: str = "/api/v1/events/ingest"
    trend_interval_s: int = 60
    required_streams: tuple[str, ...] = ("events", "status", "diagnostics")


@dataclass(frozen=True)
class EmergencyRoutingPolicy:
    """Contract for critical crash escalation routing behavior."""

    critical_event: str = "CRASH"
    max_route_latency_ms: int = 200
    fallback_route: str = "local-emergency-contact"


@dataclass(frozen=True)
class PrivacyGovernanceContract:
    """Contract for consent/events-only toggles and DSAR endpoints."""

    consent_toggle_key: str = "consent.enabled"
    events_only_key: str = "privacy.events_only_mode"
    dsar_endpoints: tuple[str, ...] = (
        "/api/v1/dsar/access-export",
        "/api/v1/dsar/correction",
        "/api/v1/dsar/delete",
    )


@dataclass(frozen=True)
class BenchmarkHarnessContract:
    """Contract for benchmarking latency and false-alert baselines."""

    report_id: str = "gp1-carry-forward-baseline"
    latency_target_ms: int = 200
    false_alert_target: float = 0.05
    runtime_hours_target: int = 8


def carry_forward_validation_targets() -> dict[str, float | int]:
    """Benchmark targets that gate GP1 carry-forward progression."""

    return {
        "alert_path_latency_ms": 200,
        "max_false_alert_rate": 0.05,
        "runtime_hours_target": 8,
    }
