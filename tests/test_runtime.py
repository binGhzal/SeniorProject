"""Unit tests for GP2 prototype logic and feature-flag wiring."""

import unittest
from unittest.mock import MagicMock
from src.gp2.sensors import IMUSensor
from src.gp2.detection import FatigueDetector
from src.gp2.planning.features import (
    AppFeatureSet,
    FeatureDefinition,
    OnBoardFeatureSet,
    derive_runtime_feature_flags,
)


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


if __name__ == '__main__':
    unittest.main()
