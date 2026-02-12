from dataclasses import dataclass
from typing import Dict


@dataclass
class PowerProfile:
    average_ma: float = 0.0
    peak_ma: float = 0.0
    standby_ma: float = 0.0


def estimate_total_current(profiles: Dict[str, PowerProfile]) -> PowerProfile:
    return PowerProfile(
        average_ma=sum(p.average_ma for p in profiles.values()),
        peak_ma=sum(p.peak_ma for p in profiles.values()),
        standby_ma=sum(p.standby_ma for p in profiles.values()),
    )
