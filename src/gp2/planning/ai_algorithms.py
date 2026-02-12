from dataclasses import dataclass


@dataclass
class AIPlan:
    approach: str = "heuristic-ear-perclos"
    requires_training_data: bool = False
    model_version: str = "v0-placeholder"


def requires_validation_dataset(plan: AIPlan) -> bool:
    return plan.approach != "heuristic-ear-perclos"
