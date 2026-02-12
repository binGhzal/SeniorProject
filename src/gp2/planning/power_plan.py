"""Power-profile models and helpers for runtime estimation and reporting."""

from dataclasses import dataclass


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


def estimate_total_current(profiles: dict[str, PowerProfile]) -> PowerProfile:
    """Aggregate current estimates from per-subsystem power profiles."""

    return PowerProfile(
        average_ma=sum(p.average_ma for p in profiles.values()),
        peak_ma=sum(p.peak_ma for p in profiles.values()),
        standby_ma=sum(p.standby_ma for p in profiles.values()),
    )


def has_valid_power_bounds(profile: PowerProfile) -> bool:
    """Validate basic electrical sanity: peak >= average >= standby >= 0."""
    return profile.peak_ma >= profile.average_ma >= profile.standby_ma >= 0


def estimate_runtime_hours(
    battery_capacity_mah: float,
    average_current_ma: float,
    derating_factor: float = 0.85,
) -> float:
    """Estimate runtime hours from battery capacity and average load current."""
    if battery_capacity_mah <= 0 or average_current_ma <= 0:
        return 0.0
    if derating_factor <= 0:
        return 0.0
    return (battery_capacity_mah * derating_factor) / average_current_ma


def required_battery_capacity_mah(
    target_runtime_h: float,
    average_current_ma: float,
    derating_factor: float = 0.85,
) -> float:
    """Estimate minimum battery capacity required for a target runtime."""
    if target_runtime_h <= 0 or average_current_ma <= 0 or derating_factor <= 0:
        return 0.0
    return (target_runtime_h * average_current_ma) / derating_factor


def regulator_margin_ok(
    regulator_max_ma: float,
    expected_peak_ma: float,
    required_margin_ratio: float = 0.2,
) -> bool:
    """Check that regulator max current provides required headroom over peak load."""
    if regulator_max_ma <= 0 or expected_peak_ma < 0 or required_margin_ratio < 0:
        return False
    required_max = expected_peak_ma * (1 + required_margin_ratio)
    return regulator_max_ma >= required_max


def meets_runtime_target(
    battery_capacity_mah: float,
    average_current_ma: float,
    target_runtime_h: float = 8.0,
    derating_factor: float = 0.85,
) -> bool:
    """Return whether estimated runtime satisfies target operating hours."""
    runtime_h = estimate_runtime_hours(battery_capacity_mah, average_current_ma, derating_factor)
    return runtime_h >= target_runtime_h
