"""Software-architecture contracts for runtime orchestration boundaries."""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Mapping, Optional


@dataclass
class RuntimeTopology:
    """Declares execution style for sensor, detection, and telemetry loops."""

    sensor_loop: str = "single-thread-polling"
    detection_loop: str = "inline"
    telemetry_loop: str = "inline"


@dataclass
class DependencyPlan:
    """Tracks required and optional runtime dependency groups."""

    runtime_libraries: List[str] = field(default_factory=lambda: ["numpy"])
    optional_libraries: List[str] = field(default_factory=lambda: ["opencv-python", "paho-mqtt"])


@dataclass(frozen=True)
class RuntimeOrchestratorContract:
    """Defines boundary callbacks for a single runtime cycle."""

    read_sensor_snapshot: Callable[[], Mapping[str, Any]]
    detect_fatigue: Callable[[Mapping[str, Any]], Mapping[str, Any]]
    publish_runtime_event: Callable[[str, Mapping[str, Any]], None]


def execute_runtime_cycle(
    contract: RuntimeOrchestratorContract,
    crash_threshold_g: float = 2.5,
) -> Dict[str, Any]:
    """Execute one orchestrator cycle using injected side-effect boundaries."""
    snapshot = dict(contract.read_sensor_snapshot())
    g_force = float(snapshot.get("g_force", 0.0))
    crash_detected = g_force > crash_threshold_g

    if crash_detected:
        contract.publish_runtime_event("CRASH", {"g_force": g_force})

    fatigue_result = dict(contract.detect_fatigue(snapshot))
    fatigue_detected = bool(fatigue_result.get("is_drowsy", False))
    if fatigue_detected:
        contract.publish_runtime_event(
            "FATIGUE",
            {
                "ear": float(fatigue_result.get("ear", 0.0)),
                "latency_ms": float(fatigue_result.get("latency_ms", 0.0)),
                "mode": fatigue_result.get("mode", "heuristic-ear-perclos"),
            },
        )

    status_payload: Dict[str, Any] = {
        "g_force": g_force,
        "perclos": float(fatigue_result.get("perclos", 0.0)),
        "fatigue": fatigue_detected,
        "ai_metrics": {
            "mode": fatigue_result.get("mode", "heuristic-ear-perclos"),
            "latency_ms": float(fatigue_result.get("latency_ms", 0.0)),
            "false_alert": bool(fatigue_result.get("false_alert", False)),
        },
    }
    contract.publish_runtime_event("STATUS", status_payload)

    return {
        "crash_detected": crash_detected,
        "fatigue_detected": fatigue_detected,
        "status_payload": status_payload,
    }


def side_effect_boundaries() -> Dict[str, str]:
    """Returns module ownership map to keep I/O side effects isolated."""
    return {
        "sensor_io": "src/gp2/sensors.py",
        "network_io": "src/gp2/telemetry.py",
        "orchestrator": "src/gp2/main.py",
        "detection_logic": "src/gp2/detection.py",
        "planning_contracts": "src/gp2/planning/software_architecture.py",
    }


def architecture_ready_for_mvp(topology: RuntimeTopology, deps: DependencyPlan) -> bool:
    """Return whether the declared topology and dependencies satisfy MVP readiness."""
    return bool(topology.sensor_loop and deps.runtime_libraries)


def dependency_versions() -> Dict[str, Optional[str]]:
    """Declares expected runtime dependency versions for documentation/tests."""
    return {
        "python": "3.11+",
        "numpy": "1.26+",
        "opencv-python": None,
        "paho-mqtt": None,
        "scipy": None,
    }
