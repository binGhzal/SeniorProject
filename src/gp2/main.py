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
# import dlib # Required for actual landmark detection


def main():
    """Initialize modules and execute the monitoring loop."""
    # 1. Hardware Bring-up [cite: 379]
    imu = IMUSensor()
    cam = CameraModule()
    ir = IRSys()
    mqtt = TelemetryClient()
    detector = FatigueDetector()
    feature_definition = build_default_feature_definition()
    runtime_flags = derive_runtime_feature_flags(feature_definition)

    # Mocking dlib predictor for code structure (Actual implementation needs .dat file)
    # predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    print("System Initialized. Starting Monitoring...")
    ir.set_brightness(50)  # Set IR LEDs to 50%

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
                # Here you would lock the circular video buffer

            # C. AI Processing (Simulated landmarks for structure)
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # rects = detector_dlib(gray, 0)
            # landmarks = predictor(gray, rect) ...

            # For this code snippet, we simulate landmarks
            drowsy = False
            ear = 0.0
            if runtime_flags.enable_fatigue_detection:
                mock_landmarks = np.zeros((68, 2))
                drowsy, ear = detector.analyze_frame(mock_landmarks)

            if drowsy:
                print(f"FATIGUE ALERT! EAR: {ear:.2f}")
                if runtime_flags.enable_alert_publish:
                    mqtt.send_alert("FATIGUE", ear)

            # D. Telemetry Heartbeat
            if runtime_flags.enable_status_telemetry:
                mqtt.send_telemetry(perclos=0.05, g_force=total_g)

            # Maintenance loop delay
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        cam.release()
        ir.cleanup()


if __name__ == "__main__":
    main()