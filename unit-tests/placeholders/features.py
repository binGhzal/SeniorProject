from dataclasses import dataclass, field
from typing import List


@dataclass
class AppFeatureSet:
    pairing: bool = False
    live_status: bool = False
    alerts_center: bool = False
    trip_history: bool = False


@dataclass
class OnBoardFeatureSet:
    crash_detection: bool = True
    fatigue_detection: bool = True
    sensor_self_test: bool = False
    local_buffering: bool = False


@dataclass
class FeatureDefinition:
    app_features: AppFeatureSet = field(default_factory=AppFeatureSet)
    board_features: OnBoardFeatureSet = field(default_factory=OnBoardFeatureSet)
    open_questions: List[str] = field(default_factory=list)


def build_default_feature_definition() -> FeatureDefinition:
    return FeatureDefinition(
        open_questions=[
            "Confirm target client platform (mobile/web/both)",
            "Confirm emergency contact notification flow",
        ]
    )
