"""Main runtime loop for the GP2 smart-helmet prototype."""

import time
import numpy as np
from .sensors import IMUSensor, CameraModule, IRSys
from .detection import FatigueDetector
from .telemetry import TelemetryClient
from .planning.features import (
    build_default_feature_definition,
    derive_runtime_feature_flags,
)
from .planning.power_plan import (
    PowerProfile,
    estimate_total_current,
    has_valid_power_bounds,
)
from .planning.connectivity import ConnectivityConfig, validate_connectivity_config
from .planning.storage_strategy import LocalStorageBuffer
from .planning.storage_strategy import StorageEvent
from .planning.storage_strategy import StoragePolicy
from .planning.ai_algorithms import build_default_ai_plan, detector_mode
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
    last_status_publish_ts = 0.0

    try:
        while True:
            # A. Read Sensors
            _frame = cam.get_frame()
            ax, ay, az = imu.read_accel()
            total_g = np.sqrt(ax**2 + ay**2 + az**2)

            # B. Crash Detection (High G Event) [cite: 228]
            if runtime_flags.enable_crash_detection and total_g > 2.5:  # 2.5G threshold
                print(f"CRASH DETECTED! G-Force: {total_g:.2f}")
                if runtime_flags.enable_alert_publish:
                    mqtt.send_alert("CRASH", total_g)
                local_storage.add_event(
                    StorageEvent(
                        event_type="alert_crash",
                        payload={"g_force": total_g},
                    )
                )
                # Here you would lock the circular video buffer

            # C. AI Processing (Simulated landmarks for structure)
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # rects = detector_dlib(gray, 0)
            # landmarks = predictor(gray, rect) ...

            # For this code snippet, we simulate landmarks
            drowsy = False
            ear = 0.0
            ai_metrics = {
                "mode": active_detector_mode,
                "latency_ms": 0.0,
                "false_alert": False,
            }
            if runtime_flags.enable_fatigue_detection:
                mock_landmarks = np.zeros((68, 2))
                result = detector.analyze_frame_with_metrics(
                    mock_landmarks,
                    mode=active_detector_mode,
                )
                drowsy = bool(result["is_drowsy"])
                ear = float(result["ear"])
                ai_metrics = {
                    "mode": result["mode"],
                    "latency_ms": result["latency_ms"],
                    "false_alert": result["false_alert"],
                }

            if drowsy:
                print(f"FATIGUE ALERT! EAR: {ear:.2f}")
                if runtime_flags.enable_alert_publish:
                    mqtt.send_alert("FATIGUE", ear)
                local_storage.add_event(
                    StorageEvent(
                        event_type="alert_fatigue",
                        payload={"ear": ear},
                    )
                )

            # D. Telemetry Heartbeat
            current_ts = time.time()
            should_publish_status = (
                runtime_flags.enable_status_telemetry
                and (current_ts - last_status_publish_ts)
                >= connectivity_config.telemetry_interval_s
            )
            if should_publish_status:
                mqtt.send_telemetry(
                    perclos=0.05,
                    g_force=total_g,
                    sensor_health=sensor_health,
                    power_profile=power_profile,
                    ai_metrics=ai_metrics,
                )
                local_storage.add_event(
                    StorageEvent(
                        event_type="status",
                        payload={
                            "perclos": 0.05,
                            "g_force": total_g,
                            "sensor_health": sensor_health,
                            "power_profile": power_profile,
                            "ai_metrics": ai_metrics,
                        },
                    )
                )
                last_status_publish_ts = current_ts

            # Maintenance loop delay
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        cam.release()
        ir.cleanup()


if __name__ == "__main__":
    main()
