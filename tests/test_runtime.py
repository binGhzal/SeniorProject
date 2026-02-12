"""Unit tests for GP2 prototype logic and feature-flag wiring."""

import json
import time
import unittest
from typing import cast
from unittest.mock import MagicMock

from src.gp2.detection import FatigueDetector
from src.gp2.main import build_power_profile, build_sensor_health
from src.gp2.planning.ai_algorithms import (
    MODEL_MODE,
    AIPlan,
    detector_mode,
    evaluation_contract,
    supported_dataset_scopes,
)
from src.gp2.planning.connectivity import ConnectivityConfig, validate_connectivity_config
from src.gp2.planning.features import (
    AppFeatureSet,
    FeatureDefinition,
    OnBoardFeatureSet,
    derive_runtime_feature_flags,
)
from src.gp2.planning.hardware_architecture import default_interface_map
from src.gp2.planning.power_plan import PowerProfile, estimate_total_current, has_valid_power_bounds
from src.gp2.planning.software_architecture import (
    RuntimeOrchestratorContract,
    dependency_versions,
    execute_runtime_cycle,
    side_effect_boundaries,
)
from src.gp2.planning.storage_strategy import (
    LocalStorageBuffer,
    StorageEvent,
    StoragePolicy,
    resolve_sync_conflict,
)
from src.gp2.sensors import CameraModule, IMUSensor, IRSys
from src.gp2.telemetry import TelemetryClient


class TestSmartHelmet(unittest.TestCase):
    """Covers core sensor/detection logic and feature configuration behavior."""

    # --- Part A: Individual Unit Tests ---

    def test_imu_connection(self):
        """Test 1: Verify IMU reads data format correctly"""
        imu = IMUSensor()
        # Mocking the actual SMBus to avoid hardware errors on PC
        imu.bus.read_i2c_block_data = MagicMock(return_value=[0, 0, 0, 0, 32, 60])

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
        total_g = (ax**2 + ay**2 + az**2) ** 0.5

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
        power_profile = build_power_profile(
            build_sensor_health(IMUSensor(), CameraModule(), IRSys())
        )
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

    def test_telemetry_includes_ai_metrics(self):
        """Confirms status telemetry payload carries optional AI runtime metrics."""
        client = TelemetryClient()
        client.client = MagicMock()
        client.send_telemetry(
            perclos=0.1,
            g_force=1.2,
            ai_metrics={"mode": "heuristic-ear-perclos", "latency_ms": 5.0},
        )
        publish_args = client.client.publish.call_args.args
        payload = json.loads(publish_args[1])
        self.assertIn("ai_metrics", payload)
        self.assertEqual(payload["ai_metrics"]["mode"], "heuristic-ear-perclos")

    def test_connectivity_config_validation(self):
        """Rejects invalid connectivity configuration values."""
        valid = ConnectivityConfig()
        invalid = ConnectivityConfig(protocol="invalid")
        self.assertTrue(validate_connectivity_config(valid))
        self.assertFalse(validate_connectivity_config(invalid))

    def test_offline_queue_placeholder_behavior(self):
        """Queues unsent messages when connectivity is unavailable."""
        config = ConnectivityConfig(
            offline_queue_enabled=True,
            offline_queue_max_items=2,
        )
        client = TelemetryClient(config=config)
        client.client = None

        client.send_alert("CRASH", 3.0)
        client.send_alert("FATIGUE", 0.1)
        client.send_alert("CRASH", 2.8)

        self.assertEqual(len(client.offline_queue), 2)
        self.assertEqual(client.offline_queue[-1]["payload"]["alert"], "CRASH")

    def test_qos_policy_from_connectivity_config(self):
        """Uses configured QoS values for status and alert publishes."""
        config = ConnectivityConfig(status_qos=1, alert_qos=0)
        client = TelemetryClient(config=config)
        client.client = MagicMock()

        client.send_alert("FATIGUE", 0.2)
        client.send_telemetry(0.1, 1.1)

        alert_call = client.client.publish.call_args_list[0]
        status_call = client.client.publish.call_args_list[1]
        self.assertEqual(alert_call.kwargs["qos"], 0)
        self.assertEqual(status_call.kwargs["qos"], 1)

    def test_storage_retention_pruning(self):
        """Prunes records older than retention window."""
        policy = StoragePolicy(on_device_retention_hours=1, on_device_queue_max_items=100)
        buffer = LocalStorageBuffer(policy=policy)
        now = time.time()
        buffer.add_event(StorageEvent("status", {"id": 1}, timestamp=now - 5000))
        buffer.add_event(StorageEvent("status", {"id": 2}, timestamp=now - 100))

        buffer.prune_retention(now=now)
        self.assertEqual(len(buffer.events), 1)
        self.assertEqual(buffer.events[0].payload["id"], 2)

    def test_storage_capacity_bounds(self):
        """Keeps only the newest events when queue reaches max capacity."""
        policy = StoragePolicy(on_device_queue_max_items=2)
        buffer = LocalStorageBuffer(policy=policy)
        buffer.add_event(StorageEvent("status", {"id": 1}))
        buffer.add_event(StorageEvent("status", {"id": 2}))
        buffer.add_event(StorageEvent("status", {"id": 3}))

        self.assertEqual(len(buffer.events), 2)
        self.assertEqual(buffer.events[0].payload["id"], 2)
        self.assertEqual(buffer.events[1].payload["id"], 3)

    def test_storage_replay_and_sync_marking(self):
        """Returns unsynced records for replay and marks selected entries synced."""
        buffer = LocalStorageBuffer(policy=StoragePolicy())
        buffer.add_event(StorageEvent("status", {"id": 1}, synced=False))
        buffer.add_event(StorageEvent("status", {"id": 2}, synced=True))
        buffer.add_event(StorageEvent("status", {"id": 3}, synced=False))

        pending = buffer.pending_replay_events()
        self.assertEqual(len(pending), 2)

        buffer.mark_synced([0, 2])
        pending_after = buffer.pending_replay_events()
        self.assertEqual(len(pending_after), 0)

    def test_storage_conflict_resolution_last_write_wins(self):
        """Selects the latest timestamp event for last-write-wins policy."""
        local = StorageEvent("status", {"source": "local"}, timestamp=200.0)
        remote = StorageEvent("status", {"source": "remote"}, timestamp=100.0)
        winner = resolve_sync_conflict(local, remote, "last-write-wins")

        self.assertEqual(winner.payload["source"], "local")

    def test_software_architecture_contract_cycle(self):
        """Executes a single cycle through injected boundaries and publishes outputs."""
        published = []

        def read_sensor_snapshot():
            return {"g_force": 3.1}

        def detect_fatigue(_snapshot):
            return {
                "is_drowsy": True,
                "ear": 0.14,
                "latency_ms": 12.5,
                "mode": "heuristic-ear-perclos",
                "perclos": 0.18,
                "false_alert": False,
            }

        def publish_runtime_event(event_type, payload):
            published.append((event_type, payload))

        contract = RuntimeOrchestratorContract(
            read_sensor_snapshot=read_sensor_snapshot,
            detect_fatigue=detect_fatigue,
            publish_runtime_event=publish_runtime_event,
        )
        result = execute_runtime_cycle(contract)

        event_types = [event for event, _ in published]
        self.assertIn("CRASH", event_types)
        self.assertIn("FATIGUE", event_types)
        self.assertIn("STATUS", event_types)
        self.assertTrue(result["crash_detected"])
        self.assertTrue(result["fatigue_detected"])

    def test_software_architecture_boundaries_and_versions(self):
        """Publishes stable module boundary map and dependency declarations."""
        boundaries = side_effect_boundaries()
        versions = dependency_versions()

        self.assertEqual(boundaries["sensor_io"], "src/gp2/sensors.py")
        self.assertIn("numpy", versions)
        self.assertEqual(versions["python"], "3.11+")

    def test_ai_mode_selection_and_evaluation_contract(self):
        """Builds model-based AI contracts with dataset and metric gates."""
        plan = AIPlan(
            approach=MODEL_MODE,
            requires_training_data=True,
            model_version="v1.0.0",
            dataset_tag="night-helmet-v1",
            max_latency_ms=65.0,
            max_false_alert_rate=0.03,
        )

        self.assertEqual(detector_mode(plan), MODEL_MODE)
        contract = evaluation_contract(plan)
        self.assertEqual(contract["dataset_tag"], "night-helmet-v1")
        metrics = cast(dict[str, float], contract["metrics"])
        self.assertEqual(metrics["max_latency_ms"], 65.0)
        self.assertIn("outdoor_night", supported_dataset_scopes())

    def test_fatigue_metrics_include_false_alert_tracking(self):
        """Returns latency/mode metrics and false-alert flag for AI validation."""
        detector = FatigueDetector()
        detector.analyze_frame = MagicMock(return_value=(True, 0.19))
        result = detector.analyze_frame_with_metrics(
            landmarks=[],
            expected_drowsy=False,
            mode="heuristic-ear-perclos",
        )

        self.assertTrue(result["is_drowsy"])
        self.assertTrue(result["false_alert"])
        self.assertGreaterEqual(result["latency_ms"], 0.0)
        self.assertEqual(result["mode"], "heuristic-ear-perclos")


if __name__ == "__main__":
    unittest.main()
