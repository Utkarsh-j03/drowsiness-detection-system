import time
from location_service import LocationService
from dataclasses import dataclass, field
from config import *
from alarm import AlarmState, stop_alarm
from detection.face_eye_detector import load_cascades, detect_face_and_eyes
from detection.state_manager import DetectionState, update_detection_state
import cv2

@dataclass
class LocationState:
    text: str = "Fetching location..."
    coordinates_text: str = "Coordinates: unavailable"


def setup_camera(index=CAMERA_INDEX):
    """Open the webcam and apply a reasonable resolution."""
    camera = cv2.VideoCapture(index)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    return camera


def draw_detections(frame, face_box, eyes):
    """Draw face and eye rectangles to visualize detections."""
    if face_box is None:
        return

    x, y, w, h = face_box
    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 200, 0), 2)

    for ex, ey, ew, eh in eyes[:2]:
        cv2.rectangle(frame, (x + ex, y + ey), (x + ex + ew, y + ey + eh), (0, 255, 255), 2)

def draw_status_panel(frame, status_text, status_color, alert_text, closed_duration, face_box, eyes, detection_state, alarm_state,location_text, coordinates_text):
    """Draw a compact status panel."""
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    eye_count = min(len(eyes), 2) if face_box is not None else 0
    alarm_text = "ON" if alarm_state.is_running else "OFF"

    cv2.rectangle(frame, (10, 10), (420, 170), (25, 25, 25), -1)
    cv2.rectangle(frame, (10, 10), (420, 170), (80, 80, 80), 2)

    cv2.putText(frame, "Drowsiness Monitor", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(frame, f"Time: {current_time}", (20, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
    cv2.putText(frame, f"Status: {status_text}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, status_color, 2)
    cv2.putText(frame, f"Eyes: {eye_count}", (20, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (220, 220, 220), 1)
    cv2.putText(frame, f"Alarm: {alarm_text}", (140, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (220, 220, 220), 1)
    cv2.putText(frame, f"Alerts: {detection_state.total_alerts}", (260, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (220, 220, 220), 1)
    cv2.putText(frame, location_text[:55], (20, 130),cv2.FONT_HERSHEY_SIMPLEX, 0.43, (180, 255, 180), 1)
    cv2.putText(frame, coordinates_text[:55], (20, 150),cv2.FONT_HERSHEY_SIMPLEX, 0.4, (180, 255, 180), 1)

    if closed_duration > 0:
        cv2.putText(frame, f"Closed: {closed_duration:.1f}s", (460, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    if alert_text:
        cv2.rectangle(frame, (450, 55), (930, 110), (0, 0, 255), -1)
        cv2.putText(frame, alert_text, (490, 92), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

    cv2.putText(frame, "Press Q or Esc to exit", (20, frame.shape[0] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (240, 240, 240), 1)


def should_close_window(window_name):
    """Allow exit using Q, Esc, or the window close button."""
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        return True

    try:
        if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            return True
    except cv2.error:
        return True

    return False


def main():
    print("Starting Driver Drowsiness Detection System...")
    print("Press 'q' or 'Esc' to quit.")

    try:
        face_cascade, eye_cascade = load_cascades()
    except RuntimeError as error:
        print(f"Error: {error}")
        return

    camera = setup_camera()
    if not camera.isOpened():
        print("Error: Could not open webcam.")
        print("Check if your camera is connected and not being used by another app.")
        print("If needed, change CAMERA_INDEX from 0 to 1 in app.py.")
        return

    detection_state = DetectionState()
    alarm_state = AlarmState()

    location_service = LocationService(google_api_key=None)  

    try:
        while True:
            success, frame = camera.read()
            if not success:
                print("Error: Failed to read frame from webcam.")
                break

            frame = cv2.flip(frame, 1)
            face_box, eyes = detect_face_and_eyes(frame, face_cascade, eye_cascade)
            draw_detections(frame, face_box, eyes)

            status_text, status_color, alert_text, closed_duration = update_detection_state(
                face_box, eyes, detection_state, alarm_state
            )

            if not hasattr(main, "last_location_time"):
                main.last_location_time = 0
                main.location_data = None

            if time.time() - main.last_location_time > 5:
                main.location_data = location_service.get_best_location()
                main.last_location_time = time.time()

            location_data = main.location_data

            if location_data:
                if location_data["source"] == "IP":
                    location_text = f"{location_data.get('city')}, {location_data.get('region')}, {location_data.get('country')}"
                else:
                    location_text = f"{location_data['lat']:.4f}, {location_data['lon']:.4f}"

                coordinates_text = f"{location_data['source']} | {location_data['accuracy']}"
            else:
                location_text = "Location unavailable"
                coordinates_text = ""

            draw_status_panel(
                frame,
                status_text,
                status_color,
                alert_text,
                closed_duration,
                face_box,
                eyes,
                detection_state,
                alarm_state,
                location_text,
                coordinates_text
            )

            cv2.imshow(WINDOW_NAME, frame)

            if should_close_window(WINDOW_NAME):
                break
    finally:
        stop_alarm(alarm_state)
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
