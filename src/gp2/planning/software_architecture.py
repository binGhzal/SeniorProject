from dataclasses import dataclass, field
from typing import List


@dataclass
class RuntimeTopology:
    sensor_loop: str = "single-thread-polling"
    detection_loop: str = "inline"
    telemetry_loop: str = "inline"


@dataclass
class DependencyPlan:
    runtime_libraries: List[str] = field(default_factory=lambda: ["numpy"])
    optional_libraries: List[str] = field(default_factory=lambda: ["opencv-python", "paho-mqtt"])


def architecture_ready_for_mvp(topology: RuntimeTopology, deps: DependencyPlan) -> bool:
    return bool(topology.sensor_loop and deps.runtime_libraries)
