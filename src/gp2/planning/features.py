"""Feature definitions and runtime flag derivation for the GP2 prototype."""

from dataclasses import dataclass, field


@dataclass
class AppFeatureSet:
    """Application-side feature toggles."""

    pairing: bool = False
    live_status: bool = False
    alerts_center: bool = False
    trip_history: bool = False


@dataclass
class OnBoardFeatureSet:
    """Embedded-board feature toggles."""

    crash_detection: bool = True
    fatigue_detection: bool = True
    sensor_self_test: bool = False
    local_buffering: bool = False


@dataclass
class FeatureDefinition:
    """Combined feature definition for app and board scopes."""

    app_features: AppFeatureSet = field(default_factory=AppFeatureSet)
    board_features: OnBoardFeatureSet = field(default_factory=OnBoardFeatureSet)
    open_questions: list[str] = field(default_factory=list)


@dataclass
class RuntimeFeatureFlags:
    """Runtime-ready feature gates consumed by the monitoring loop."""

    enable_crash_detection: bool
    enable_fatigue_detection: bool
    enable_alert_publish: bool
    enable_status_telemetry: bool


def build_default_feature_definition() -> FeatureDefinition:
    """Build a default feature profile for prototype execution."""

    return FeatureDefinition(
        app_features=AppFeatureSet(
            live_status=True,
            alerts_center=True,
        ),
        open_questions=[
            "Confirm target client platform (mobile/web/both)",
            "Confirm emergency contact notification flow",
        ],
    )


def derive_runtime_feature_flags(feature_definition: FeatureDefinition) -> RuntimeFeatureFlags:
    """Map high-level feature settings to explicit runtime gates."""

    return RuntimeFeatureFlags(
        enable_crash_detection=feature_definition.board_features.crash_detection,
        enable_fatigue_detection=feature_definition.board_features.fatigue_detection,
        enable_alert_publish=feature_definition.app_features.alerts_center,
        enable_status_telemetry=feature_definition.app_features.live_status,
    )
