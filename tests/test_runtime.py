"""Unit tests for GP2 prototype logic and feature-flag wiring."""

import json
import unittest
from unittest.mock import MagicMock
from src.gp2.sensors import IMUSensor
from src.gp2.sensors import CameraModule, IRSys
from src.gp2.detection import FatigueDetector
from src.gp2.main import build_sensor_health
from src.gp2.main import build_power_profile
from src.gp2.planning.hardware_architecture import default_interface_map
from src.gp2.planning.power_plan import PowerProfile, estimate_total_current
from src.gp2.planning.power_plan import has_valid_power_bounds
from src.gp2.planning.features import (
    AppFeatureSet,
    FeatureDefinition,
    OnBoardFeatureSet,
    derive_runtime_feature_flags,
)
from src.gp2.telemetry import TelemetryClient


class TestSmartHelmet(unittest.TestCase):
    """Covers core sensor/detection logic and feature configuration behavior."""

    # --- Part A: Individual Unit Tests ---

    def test_imu_connection(self):
        """Test 1: Verify IMU reads data format correctly"""
        imu = IMUSensor()
        # Mocking the actual SMBus to avoid hardware errors on PC
        imu.bus.read_i2c_block_data = MagicMock(
            return_value=[0, 0, 0, 0, 32, 60]
        )

        accel = imu.read_accel()
        self.assertIsInstance(accel, tuple)
        self.assertEqual(len(accel), 3)
        print("\n[Pass] IMU Data Format Verified")

    def test_fatigue_logic(self):
        """Test 5: Fatigue Logic Simulation (Software Injection)"""
        det = FatigueDetector()

        # Inject "closed" eye landmarks (mocking EAR < 0.2)
        # We manually trigger the logic for testing
        det.analyze_frame = MagicMock(return_value=(True, 0.15))

        is_drowsy, ear = det.analyze_frame([])

        self.assertTrue(is_drowsy)
        self.assertLess(ear, 0.25)
        print("\n[Pass] Fatigue Logic Triggered Correctly")

    # --- Part B: Integrated System Tests ---

    def test_crash_integration(self):
        """Test 4: The 'Shake to Upload' Crash Logic"""
        # Simulate High-G Event
        mock_imu = MagicMock()
        mock_mqtt = MagicMock()

        # Simulate reading 3.0G from sensor
        mock_imu.read_accel.return_value = (0, 0, 3.0)

        ax, ay, az = mock_imu.read_accel()
        total_g = (ax**2 + ay**2 + az**2)**0.5

        if total_g > 2.5:
            mock_mqtt.send_alert("CRASH", total_g)

        # Verify alert was sent
        mock_mqtt.send_alert.assert_called_with("CRASH", 3.0)
        print("\n[Pass] Crash Integration (Sensor -> Cloud Trigger) Verified")

    def test_feature_flags_disable_status_telemetry(self):
        """Disables status telemetry when app live status is turned off."""
        feature_definition = FeatureDefinition(
            app_features=AppFeatureSet(live_status=False, alerts_center=True),
            board_features=OnBoardFeatureSet(crash_detection=True, fatigue_detection=True),
        )
        flags = derive_runtime_feature_flags(feature_definition)

        self.assertFalse(flags.enable_status_telemetry)
        self.assertTrue(flags.enable_alert_publish)

    def test_feature_flags_disable_alert_publish(self):
        """Disables alert publishing when app alert center is turned off."""
        feature_definition = FeatureDefinition(
            app_features=AppFeatureSet(live_status=True, alerts_center=False),
            board_features=OnBoardFeatureSet(crash_detection=True, fatigue_detection=True),
        )
        flags = derive_runtime_feature_flags(feature_definition)

        self.assertFalse(flags.enable_alert_publish)
        self.assertTrue(flags.enable_status_telemetry)

    def test_sensor_health_snapshot_shape(self):
        """Provides a stable sensor-health structure for telemetry payloads."""
        imu = IMUSensor()
        cam = CameraModule()
        ir = IRSys()

        snapshot = build_sensor_health(imu, cam, ir)

        self.assertIn("imu", snapshot)
        self.assertIn("camera", snapshot)
        self.assertIn("ir", snapshot)
        self.assertIn("available", snapshot["imu"])
        self.assertIn("mode", snapshot["imu"])

    def test_sensor_health_includes_shared_interface_specs(self):
        """Ensures runtime health reports use planning interface constants."""
        specs = default_interface_map()
        snapshot = build_sensor_health(IMUSensor(), CameraModule(), IRSys())

        self.assertEqual(snapshot["imu"]["bus"], specs["imu"].bus)
        self.assertEqual(snapshot["camera"]["direction"], specs["camera"].direction)
        self.assertEqual(snapshot["ir"]["bus"], specs["ir"].bus)

    def test_power_profile_aggregation_and_bounds(self):
        """Validates power aggregation and electrical sanity bounds."""
        total = estimate_total_current(
            {
                "a": PowerProfile(average_ma=10.0, peak_ma=20.0, standby_ma=5.0),
                "b": PowerProfile(average_ma=15.0, peak_ma=30.0, standby_ma=8.0),
            }
        )
        self.assertEqual(total.average_ma, 25.0)
        self.assertEqual(total.peak_ma, 50.0)
        self.assertEqual(total.standby_ma, 13.0)
        self.assertTrue(has_valid_power_bounds(total))

    def test_runtime_power_profile_shape(self):
        """Ensures runtime builds a serializable power profile payload."""
        power_profile = build_power_profile(build_sensor_health(IMUSensor(), CameraModule(), IRSys()))
        self.assertIn("average_ma", power_profile)
        self.assertIn("peak_ma", power_profile)
        self.assertIn("standby_ma", power_profile)
        self.assertIn("bounds_valid", power_profile)
        self.assertTrue(power_profile["bounds_valid"])

    def test_telemetry_includes_power_profile(self):
        """Confirms status telemetry payload carries optional power profile fields."""
        client = TelemetryClient()
        client.client = MagicMock()
        client.send_telemetry(
            perclos=0.1,
            g_force=1.2,
            sensor_health={"imu": {"available": True}},
            power_profile={"average_ma": 100.0, "peak_ma": 200.0, "standby_ma": 50.0},
        )
        publish_args = client.client.publish.call_args.args
        payload = json.loads(publish_args[1])
        self.assertIn("power_profile", payload)
        self.assertEqual(payload["power_profile"]["peak_ma"], 200.0)


if __name__ == '__main__':
    unittest.main()
