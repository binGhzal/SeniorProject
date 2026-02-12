"""Validation helpers for hardware and power evidence closeout checks."""

from dataclasses import dataclass


@dataclass(frozen=True)
class HardwareEvidence:
    """Captures hardware verification evidence status flags."""

    board_sku_confirmed: bool
    imu_camera_confirmed: bool
    pin_map_finalized: bool
    startup_sequence_verified: bool


@dataclass(frozen=True)
class PowerEvidence:
    """Captures power validation evidence status flags and measured values."""

    currents_measured: bool
    runtime_validated: bool
    protection_verified: bool
    total_average_ma: float = 0.0
    total_peak_ma: float = 0.0
    estimated_runtime_h: float = 0.0


def hardware_closeout_ready(evidence: HardwareEvidence) -> bool:
    """Return whether all hardware architecture closeout checks are satisfied."""

    return (
        evidence.board_sku_confirmed
        and evidence.imu_camera_confirmed
        and evidence.pin_map_finalized
        and evidence.startup_sequence_verified
    )


def power_closeout_ready(evidence: PowerEvidence, runtime_target_h: float = 8.0) -> bool:
    """Return whether power closeout checks satisfy runtime and protection criteria."""

    return (
        evidence.currents_measured
        and evidence.runtime_validated
        and evidence.protection_verified
        and evidence.estimated_runtime_h >= runtime_target_h
        and evidence.total_average_ma >= 0
        and evidence.total_peak_ma >= evidence.total_average_ma
    )


def closeout_summary(
    hardware: HardwareEvidence,
    power: PowerEvidence,
) -> dict[str, bool]:
    """Return a compact summary for TODO closeout dashboards/reports."""

    return {
        "todo_02_ready": hardware_closeout_ready(hardware),
        "todo_03_ready": power_closeout_ready(power),
        "overall_ready": hardware_closeout_ready(hardware) and power_closeout_ready(power),
    }
