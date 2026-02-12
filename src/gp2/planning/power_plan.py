"""Power-profile models and helpers for runtime estimation and reporting."""

from dataclasses import dataclass
from typing import Dict


@dataclass
class PowerProfile:
    """Represents average, peak, and standby current estimates in mA."""

    average_ma: float = 0.0
    peak_ma: float = 0.0
    standby_ma: float = 0.0

    def as_dict(self):
        """Return a JSON-serializable dictionary representation."""
        return {
            "average_ma": self.average_ma,
            "peak_ma": self.peak_ma,
            "standby_ma": self.standby_ma,
        }


def estimate_total_current(profiles: Dict[str, PowerProfile]) -> PowerProfile:
    """Aggregate current estimates from per-subsystem power profiles."""

    return PowerProfile(
        average_ma=sum(p.average_ma for p in profiles.values()),
        peak_ma=sum(p.peak_ma for p in profiles.values()),
        standby_ma=sum(p.standby_ma for p in profiles.values()),
    )


def has_valid_power_bounds(profile: PowerProfile) -> bool:
    """Validate basic electrical sanity: peak >= average >= standby >= 0."""
    return (
        profile.peak_ma >= profile.average_ma >= profile.standby_ma >= 0
    )
