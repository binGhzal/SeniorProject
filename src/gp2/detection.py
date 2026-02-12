"""Fatigue detection logic based on EAR and rolling PERCLOS-style scoring."""

import time
import numpy as np

try:
    from scipy.spatial import distance as dist  # type: ignore
except ImportError:  # pragma: no cover
    class _Dist:
        @staticmethod
        def euclidean(a, b):
            a_arr = np.asarray(a, dtype=float)
            b_arr = np.asarray(b, dtype=float)
            return float(np.linalg.norm(a_arr - b_arr))

    dist = _Dist()

# Thresholds from report [cite: 226]
EYE_AR_THRESH = 0.25      # Below this, eye is "closed"
PERCLOS_THRESH = 0.12     # 12% fatigue threshold
EYE_AR_CONSEC_FRAMES = 3  # Frame buffer for blink consistency

def eye_aspect_ratio(eye):
    """Compute eye aspect ratio (EAR) from a 6-point eye landmark slice."""
    # Compute euclidean distances between vertical eye landmarks
    vertical_a = dist.euclidean(eye[1], eye[5])
    vertical_b = dist.euclidean(eye[2], eye[4])
    # Compute euclidean distance between horizontal eye landmarks
    horizontal = dist.euclidean(eye[0], eye[3])
    # EAR Formula
    ear = (vertical_a + vertical_b) / (2.0 * horizontal)
    return ear

class FatigueDetector:
    """Tracks rolling eye-closure state and detects fatigue events."""

    def __init__(self):
        self.counter = 0
        self.closed_frames = 0
        self.total_frames = 0
        self.perclos_buffer = [] # Circular buffer for PERCLOS window

    def analyze_frame(self, landmarks):
        """
        Input: landmarks (list of (x,y) points for eyes)
        Output: (is_drowsy, ear_value)
        """
        # Placeholder indices for 68-point model:
        # Left Eye: 36-41, Right Eye: 42-47
        left_eye = landmarks[36:42]
        right_eye = landmarks[42:48]

        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)

        # Average EAR
        ear = (left_ear + right_ear) / 2.0

        # PERCLOS Calculation Logic
        is_closed = 0
        if ear < EYE_AR_THRESH:
            self.counter += 1
            is_closed = 1
        else:
            self.counter = 0

        # Update PERCLOS buffer (e.g., last 1000 frames)
        self.perclos_buffer.append(is_closed)
        if len(self.perclos_buffer) > 1000:
            self.perclos_buffer.pop(0)

        perclos_score = sum(self.perclos_buffer) / len(self.perclos_buffer)

        # Trigger logic
        if perclos_score > PERCLOS_THRESH:
            return True, ear

        return False, ear

    def analyze_frame_with_metrics(
        self,
        landmarks,
        expected_drowsy=None,
        mode="heuristic-ear-perclos",
    ):
        """Run fatigue analysis and return latency/false-alert metadata."""
        start = time.perf_counter()
        is_drowsy, ear = self.analyze_frame(landmarks)
        latency_ms = (time.perf_counter() - start) * 1000.0
        false_alert = bool(expected_drowsy is False and is_drowsy)
        return {
            "is_drowsy": is_drowsy,
            "ear": ear,
            "latency_ms": latency_ms,
            "false_alert": false_alert,
            "mode": mode,
            "perclos": sum(self.perclos_buffer) / len(self.perclos_buffer)
            if self.perclos_buffer
            else 0.0,
        }