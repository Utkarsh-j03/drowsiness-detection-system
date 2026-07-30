import time
from dataclasses import dataclass
from config import *
from alarm import trigger_alarm, stop_alarm


@dataclass
class DetectionState:
    closed_frames: int = 0
    open_frames: int = 0
    closed_start_time: float | None = None
    total_alerts: int = 0


def update_detection_state(face_box, eyes, detection_state, alarm_state):

    if face_box is None:
        detection_state.closed_frames = 0
        detection_state.open_frames = 0
        detection_state.closed_start_time = None
        stop_alarm(alarm_state)
        return "No Face", (0, 255, 255), "", 0.0

    if len(eyes) >= 2:
        detection_state.open_frames += 1
        detection_state.closed_frames = 0

        if detection_state.open_frames >= OPEN_CONFIRMATION_FRAMES:
            detection_state.closed_start_time = None
            stop_alarm(alarm_state)

        return "Eyes Open", (0, 255, 0), "", 0.0

    detection_state.closed_frames += 1
    detection_state.open_frames = 0

    if detection_state.closed_frames >= CLOSED_CONFIRMATION_FRAMES:
        if detection_state.closed_start_time is None:
            detection_state.closed_start_time = time.time()

        closed_duration = time.time() - detection_state.closed_start_time

        if closed_duration >= CLOSED_EYES_DURATION_SECONDS:
            if not alarm_state.is_running:
                detection_state.total_alerts += 1
            trigger_alarm(alarm_state)
            return "Eyes Closed", (0, 0, 255), "DROWSINESS ALERT!", closed_duration

        return "Eyes Closed", (0, 0, 255), "", closed_duration

    return "Checking...", (0, 165, 255), "", 0.0