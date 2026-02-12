import mediapipe as mp
import cv2

# Initialize Face Mesh with "refine_landmarks" for better eye/iris precision
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True, # Critical for accurate iris/eye tracking
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Use inside your loop
results = face_mesh.process(rgb_frame)
if results.multi_face_landmarks:
    for face_landmarks in results.multi_face_landmarks:
        # Extract Landmark 159 (Upper Eyelid) and 145 (Lower Eyelid)
        # Calculate distance to determine blink
        pass