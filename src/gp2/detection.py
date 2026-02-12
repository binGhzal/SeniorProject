"""Fatigue detection logic based on EAR and rolling PERCLOS-style scoring."""

import time
from collections import deque
from typing import Any

import numpy as np

try:
    import cv2  # type: ignore
except ImportError:  # pragma: no cover
    cv2 = None

try:
    import mediapipe as mp  # type: ignore
except ImportError:  # pragma: no cover
    mp = None

LEFT_EYE_MEDIAPIPE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_MEDIAPIPE = [362, 385, 387, 263, 373, 380]

# Thresholds from report [cite: 226]
EYE_AR_THRESH = 0.25  # Below this, eye is "closed"
PERCLOS_THRESH = 0.12  # 12% fatigue threshold
EYE_AR_CONSEC_FRAMES = 3  # Frame buffer for blink consistency
PERCLOS_WINDOW_FRAMES = 1000


def create_face_mesh() -> Any:
    """Create a MediaPipe FaceMesh instance, or return None when unavailable."""
    if mp is None:
        return None

    return mp.solutions.face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )


def extract_face_landmarks(frame: Any, face_mesh: Any) -> list[Any]:
    """Process a frame and return face landmarks list if detected."""
    if face_mesh is None or frame is None:
        return []

    rgb_frame = frame
    if cv2 is not None and isinstance(frame, np.ndarray):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb_frame)
    if not results or not results.multi_face_landmarks:
        return []

    return list(results.multi_face_landmarks)


def eye_aspect_ratio(eye):
    """Compute eye aspect ratio (EAR) from a 6-point eye landmark slice."""
    eye1 = np.asarray(eye[1], dtype=float)
    eye5 = np.asarray(eye[5], dtype=float)
    eye2 = np.asarray(eye[2], dtype=float)
    eye4 = np.asarray(eye[4], dtype=float)
    eye0 = np.asarray(eye[0], dtype=float)
    eye3 = np.asarray(eye[3], dtype=float)

    # Compute euclidean distances between vertical eye landmarks
    vertical_a = float(np.linalg.norm(eye1 - eye5))
    vertical_b = float(np.linalg.norm(eye2 - eye4))
    # Compute euclidean distance between horizontal eye landmarks
    horizontal = float(np.linalg.norm(eye0 - eye3))
    if horizontal == 0:
        return 0.0
    # EAR Formula
    ear = (vertical_a + vertical_b) / (2.0 * horizontal)
    return ear


class FatigueDetector:
    """Tracks rolling eye-closure state and detects fatigue events."""

    def __init__(self):
        self.counter = 0
        self.closed_frames = 0
        self.total_frames = 0
        self.perclos_buffer = deque(maxlen=PERCLOS_WINDOW_FRAMES)
        self.face_mesh = create_face_mesh()

    def _current_perclos(self) -> float:
        if not self.perclos_buffer:
            return 0.0
        return float(sum(self.perclos_buffer) / len(self.perclos_buffer))

    def _extract_face_landmarks(self, frame):
        landmarks = extract_face_landmarks(frame, self.face_mesh)
        if not landmarks:
            return None

        return landmarks[0]

    def _extract_eye_landmarks_from_frame(self, frame):
        face_landmarks = self._extract_face_landmarks(frame)
        if face_landmarks is None:
            return None

        points = face_landmarks.landmark
        left_eye = [(points[idx].x, points[idx].y) for idx in LEFT_EYE_MEDIAPIPE]
        right_eye = [(points[idx].x, points[idx].y) for idx in RIGHT_EYE_MEDIAPIPE]
        return left_eye, right_eye

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

        # Update PERCLOS buffer for a fixed rolling window.
        self.perclos_buffer.append(is_closed)
        perclos_score = self._current_perclos()

        # Trigger logic
        if perclos_score > PERCLOS_THRESH:
            return True, ear

        return False, ear

    def analyze_frame_with_metrics(
        self,
        landmarks,
        expected_drowsy=None,
        mode="heuristic-ear-perclos",
        frame=None,
    ):
        """Run fatigue analysis and return latency/false-alert metadata."""
        start = time.perf_counter()
        landmarks_input = landmarks

        if landmarks_input is None and frame is not None:
            eye_landmarks = self._extract_eye_landmarks_from_frame(frame)
            if eye_landmarks is not None:
                left_eye, right_eye = eye_landmarks
                landmarks_input = np.zeros((68, 2), dtype=float)
                landmarks_input[36:42] = np.asarray(left_eye, dtype=float)
                landmarks_input[42:48] = np.asarray(right_eye, dtype=float)

        if landmarks_input is None:
            is_drowsy = False
            ear = 0.0
            self.perclos_buffer.append(0)
        else:
            is_drowsy, ear = self.analyze_frame(landmarks_input)

        latency_ms = (time.perf_counter() - start) * 1000.0
        false_alert = bool(expected_drowsy is False and is_drowsy)
        return {
            "is_drowsy": is_drowsy,
            "ear": ear,
            "latency_ms": latency_ms,
            "false_alert": false_alert,
            "mode": mode,
            "perclos": self._current_perclos(),
        }
