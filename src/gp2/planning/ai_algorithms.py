"""AI planning models for heuristic/model runtime selection and validation hooks."""

from dataclasses import dataclass
from typing import Dict, List


HEURISTIC_MODE = "heuristic-ear-perclos"
MODEL_MODE = "model-based"


@dataclass
class AIPlan:
    """Defines runtime AI mode and validation thresholds for rollout gating."""

    approach: str = HEURISTIC_MODE
    requires_training_data: bool = False
    model_version: str = "v0-placeholder"
    dataset_tag: str = "dataset-placeholder"
    max_latency_ms: float = 80.0
    max_false_alert_rate: float = 0.05


def requires_validation_dataset(plan: AIPlan) -> bool:
    """Return whether the selected approach requires a labeled validation dataset."""
    return plan.approach != HEURISTIC_MODE


def detector_mode(plan: AIPlan) -> str:
    """Resolves detector mode used by runtime."""
    if plan.approach == MODEL_MODE:
        return MODEL_MODE
    return HEURISTIC_MODE


def build_default_ai_plan() -> AIPlan:
    """Returns default heuristic-first AI strategy for MVP runtime."""
    return AIPlan()


def evaluation_contract(plan: AIPlan) -> Dict[str, object]:
    """Defines dataset/metrics contract for AI validation and rollout gates."""
    return {
        "mode": detector_mode(plan),
        "dataset_tag": plan.dataset_tag,
        "model_version": plan.model_version,
        "requires_training_data": plan.requires_training_data,
        "metrics": {
            "max_latency_ms": plan.max_latency_ms,
            "max_false_alert_rate": plan.max_false_alert_rate,
        },
    }


def supported_dataset_scopes() -> List[str]:
    """Enumerates dataset buckets to guide labeling and evaluation."""
    return [
        "indoor_day",
        "indoor_night",
        "outdoor_day",
        "outdoor_night",
        "helmet_with_glasses",
    ]
