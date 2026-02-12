from dataclasses import dataclass
from typing import Dict


@dataclass
class InterfaceSpec:
    bus: str
    direction: str
    notes: str = ""


def default_interface_map() -> Dict[str, InterfaceSpec]:
    return {
        "imu": InterfaceSpec(bus="I2C", direction="bidirectional", notes="Config + accel reads"),
        "camera": InterfaceSpec(bus="CSI/USB", direction="camera->board", notes="Frame streaming"),
        "ir": InterfaceSpec(bus="GPIO/PWM", direction="board->ir", notes="Brightness control"),
    }
