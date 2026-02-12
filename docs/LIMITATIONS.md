# Limitations & Future Work

## Current limitations

- **Landmark extraction not integrated**: the runtime loop uses mock landmarks, so fatigue detection is not validated on real face/eye landmarks.
- **No accuracy evaluation**: there is no dataset-based evaluation of sensitivity, specificity, or false-alarm rate.
- **Thresholds are prototype values**: EAR/PERCLOS thresholds are not calibrated for different users or lighting conditions.
- **Telemetry security is not production-ready**: the default configuration uses a public broker without TLS.
- **Hardware behavior not fully tested**: camera, IR PWM, and IMU initialization require on-device verification.

## Recommended next steps

- Integrate a real landmark pipeline (e.g., MediaPipe FaceMesh) and map indices to the EAR computation.
- Add experiments using recorded video and ground truth labels to calibrate thresholds.
- Add end-to-end tests that validate telemetry publishes using a local MQTT broker.
- Add robust error handling and health monitoring (sensor timeouts, reconnection).
- Add performance and power profiling on the target device.
