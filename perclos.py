"""Minimal PERCLOS helpers built around optional MediaPipe FaceMesh support."""

from typing import Any

try:
    import mediapipe as mp  # type: ignore
except ImportError:  # pragma: no cover
    mp = None


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


def extract_face_landmarks(rgb_frame: Any, face_mesh: Any) -> list[Any]:
    """Process a frame and return face landmarks list if detected."""
    if face_mesh is None:
        return []

    results = face_mesh.process(rgb_frame)
    if not results or not results.multi_face_landmarks:
        return []

    return list(results.multi_face_landmarks)
