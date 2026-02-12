"""Main runtime loop for the GP2 smart-helmet prototype."""

import time

import numpy as np

from .detection import FatigueDetector
from .planning.ai_algorithms import build_default_ai_plan, detector_mode
from .planning.connectivity import ConnectivityConfig, validate_connectivity_config
from .planning.features import build_default_feature_definition, derive_runtime_feature_flags
from .planning.power_plan import PowerProfile, estimate_total_current, has_valid_power_bounds
from .planning.software_architecture import RuntimeOrchestratorContract, execute_runtime_cycle
from .planning.storage_strategy import LocalStorageBuffer, StorageEvent, StoragePolicy
from .sensors import CameraModule, IMUSensor, IRSys
from .telemetry import TelemetryClient

# import dlib # Required for actual landmark detection


def build_sensor_health(imu, cam, ir):
    """Build a consolidated sensor health snapshot for telemetry."""
    return {
        "imu": imu.health_status(),
        "camera": cam.health_status(),
        "ir": ir.health_status(),
    }


def build_power_profile(sensor_health):
    """Build aggregate power profile estimates from subsystem assumptions."""
    profiles = {
        "compute": PowerProfile(average_ma=650.0, peak_ma=1200.0, standby_ma=250.0),
        "imu": PowerProfile(average_ma=8.0, peak_ma=12.0, standby_ma=4.0),
        "camera": PowerProfile(average_ma=120.0, peak_ma=200.0, standby_ma=0.0),
        "ir": PowerProfile(average_ma=90.0, peak_ma=180.0, standby_ma=0.0),
        "radio": PowerProfile(average_ma=80.0, peak_ma=220.0, standby_ma=15.0),
    }

    if sensor_health["camera"].get("available") is False:
        profiles["camera"] = PowerProfile(average_ma=0.0, peak_ma=0.0, standby_ma=0.0)
    if sensor_health["ir"].get("available") is False:
        profiles["ir"] = PowerProfile(average_ma=0.0, peak_ma=0.0, standby_ma=0.0)

    total = estimate_total_current(profiles)
    return {
        **total.as_dict(),
        "bounds_valid": has_valid_power_bounds(total),
    }


def main():
    """Initialize modules and execute the monitoring loop."""
    # 1. Hardware Bring-up [cite: 379]
    imu = IMUSensor()
    cam = CameraModule()
    ir = IRSys()
    connectivity_config = ConnectivityConfig(
        protocol="mqtt",
        telemetry_interval_s=1.0,
        max_alert_latency_s=2.0,
        offline_queue_enabled=True,
        offline_queue_max_items=200,
    )
    if not validate_connectivity_config(connectivity_config):
        raise ValueError("Invalid runtime connectivity configuration.")

    mqtt = TelemetryClient(config=connectivity_config)
    detector = FatigueDetector()
    storage_policy = StoragePolicy(
        on_device_retention_hours=24,
        on_device_queue_max_items=500,
        cloud_sync_enabled=connectivity_config.offline_queue_enabled,
    )
    local_storage = LocalStorageBuffer(policy=storage_policy)
    feature_definition = build_default_feature_definition()
    runtime_flags = derive_runtime_feature_flags(feature_definition)
    ai_plan = build_default_ai_plan()
    active_detector_mode = detector_mode(ai_plan)

    # Mocking dlib predictor for code structure (Actual implementation needs .dat file)
    # predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    print("System Initialized. Starting Monitoring...")
    ir.set_brightness(50)  # Set IR LEDs to 50%
    sensor_health = build_sensor_health(imu, cam, ir)
    power_profile = build_power_profile(sensor_health)
    runtime_state = {
        "last_status_publish_ts": 0.0,
    }

    def read_sensor_snapshot():
        frame = cam.get_frame()
        ax, ay, az = imu.read_accel()
        g_force = float(np.sqrt(ax**2 + ay**2 + az**2))
        return {
            "frame": frame,
            "g_force": g_force,
        }

    def detect_fatigue(snapshot):
        if not runtime_flags.enable_fatigue_detection:
            return {
                "is_drowsy": False,
                "ear": 0.0,
                "latency_ms": 0.0,
                "false_alert": False,
                "mode": active_detector_mode,
                "perclos": 0.0,
            }

        return detector.analyze_frame_with_metrics(
            None,
            None,
            active_detector_mode,
            snapshot.get("frame"),
        )

    def publish_runtime_event(event_type, payload):
        if event_type == "CRASH":
            g_force = float(payload.get("g_force", 0.0))
            print(f"CRASH DETECTED! G-Force: {g_force:.2f}")
            if runtime_flags.enable_alert_publish:
                mqtt.send_alert("CRASH", g_force)
            local_storage.add_event(
                StorageEvent(
                    event_type="alert_crash",
                    payload={"g_force": g_force},
                )
            )
            return

        if event_type == "FATIGUE":
            ear = float(payload.get("ear", 0.0))
            print(f"FATIGUE ALERT! EAR: {ear:.2f}")
            if runtime_flags.enable_alert_publish:
                mqtt.send_alert("FATIGUE", ear)
            local_storage.add_event(
                StorageEvent(
                    event_type="alert_fatigue",
                    payload={"ear": ear},
                )
            )
            return

        if event_type == "STATUS":
            current_ts = time.time()
            should_publish_status = (
                runtime_flags.enable_status_telemetry
                and (current_ts - runtime_state["last_status_publish_ts"])
                >= connectivity_config.telemetry_interval_s
            )
            if not should_publish_status:
                return

            ai_metrics = dict(payload.get("ai_metrics", {}))
            mqtt.send_telemetry(
                perclos=float(payload.get("perclos", 0.0)),
                g_force=float(payload.get("g_force", 0.0)),
                sensor_health=sensor_health,
                power_profile=power_profile,
                ai_metrics=ai_metrics,
            )
            local_storage.add_event(
                StorageEvent(
                    event_type="status",
                    payload={
                        "perclos": float(payload.get("perclos", 0.0)),
                        "g_force": float(payload.get("g_force", 0.0)),
                        "sensor_health": sensor_health,
                        "power_profile": power_profile,
                        "ai_metrics": ai_metrics,
                    },
                )
            )
            runtime_state["last_status_publish_ts"] = current_ts

    contract = RuntimeOrchestratorContract(
        read_sensor_snapshot=read_sensor_snapshot,
        detect_fatigue=detect_fatigue,
        publish_runtime_event=publish_runtime_event,
    )

    try:
        while True:
            execute_runtime_cycle(contract)

            # Maintenance loop delay
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        cam.release()
        ir.cleanup()


if __name__ == "__main__":
    main()
