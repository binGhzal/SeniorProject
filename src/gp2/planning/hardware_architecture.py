"""Hardware interface placeholders for task-aligned architecture planning."""

from dataclasses import dataclass
from typing import Dict


@dataclass
class InterfaceSpec:
    """Interface metadata between the board and a peripheral block."""

    bus: str
    direction: str
    notes: str = ""


def default_interface_map() -> Dict[str, InterfaceSpec]:
    """Return default peripheral interface assumptions for the prototype."""

    return {
        "imu": InterfaceSpec(bus="I2C", direction="bidirectional", notes="Config + accel reads"),
        "camera": InterfaceSpec(bus="CSI/USB", direction="camera->board", notes="Frame streaming"),
        "ir": InterfaceSpec(bus="GPIO/PWM", direction="board->ir", notes="Brightness control"),
    }
