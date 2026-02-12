# Limitations & Future Work

## Current limitations

- **Landmark extraction is optional-runtime**: MediaPipe extraction is wired,
  but behavior depends on camera quality and available optional dependencies.
- **No accuracy evaluation**: there is no dataset-based evaluation of sensitivity, specificity, or false-alarm rate.
- **Thresholds are prototype values**: EAR/PERCLOS thresholds are not calibrated for different users or lighting conditions.
- **Telemetry security is not production-ready**: the default configuration uses a public broker without TLS.
- **Hardware behavior not fully tested**: camera, IR PWM, and IMU initialization require on-device verification.
- **GP1 scope partially deferred**: EEG and distraction/head-pose detection are still planned, not yet part of runtime MVP.

## Recommended next steps

- Integrate a real landmark pipeline (e.g., MediaPipe FaceMesh) and map indices to the EAR computation.
- Add experiments using recorded video and ground truth labels to calibrate thresholds.
- Add end-to-end tests that validate telemetry publishes using a local MQTT broker.
- Add robust error handling and health monitoring (sensor timeouts, reconnection).
- Add performance and power profiling on the target device.
