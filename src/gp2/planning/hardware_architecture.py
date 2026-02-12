"""Hardware interface placeholders for task-aligned architecture planning."""

from dataclasses import dataclass
from typing import Dict


INTERFACE_IMU = "imu"
INTERFACE_CAMERA = "camera"
INTERFACE_IR = "ir"


@dataclass
class InterfaceSpec:
    """Interface metadata between the board and a peripheral block."""

    bus: str
    direction: str
    notes: str = ""


def default_interface_map() -> Dict[str, InterfaceSpec]:
    """Return default peripheral interface assumptions for the prototype."""

    return {
        INTERFACE_IMU: InterfaceSpec(
            bus="I2C",
            direction="bidirectional",
            notes="Config + accel reads",
        ),
        INTERFACE_CAMERA: InterfaceSpec(
            bus="CSI/USB",
            direction="camera->board",
            notes="Frame streaming",
        ),
        INTERFACE_IR: InterfaceSpec(
            bus="GPIO/PWM",
            direction="board->ir",
            notes="Brightness control",
        ),
    }


def interface_spec(name: str) -> InterfaceSpec:
    """Return the interface specification for a known peripheral name."""
    return default_interface_map()[name]
