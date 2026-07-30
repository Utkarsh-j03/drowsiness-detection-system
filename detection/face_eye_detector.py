import cv2
from config import *

def load_cascades():
    face_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    eye_path = cv2.data.haarcascades + "haarcascade_eye_tree_eyeglasses.xml"

    face_cascade = cv2.CascadeClassifier(face_path)
    eye_cascade = cv2.CascadeClassifier(eye_path)

    if face_cascade.empty() or eye_cascade.empty():
        raise RuntimeError("Could not load Haar cascade files.")

    return face_cascade, eye_cascade


def detect_face_and_eyes(frame, face_cascade, eye_cascade):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray_frame,
        scaleFactor=FACE_SCALE_FACTOR,
        minNeighbors=FACE_MIN_NEIGHBORS,
        minSize=(120, 120),
    )

    if len(faces) == 0:
        return None, []

    largest_face = max(faces, key=lambda f: f[2] * f[3])
    x, y, w, h = largest_face

    face_roi_gray = gray_frame[y : y + h, x : x + w]
    upper_half = face_roi_gray[0 : h // 2, :]

    eyes = eye_cascade.detectMultiScale(
        upper_half,
        scaleFactor=EYE_SCALE_FACTOR,
        minNeighbors=EYE_MIN_NEIGHBORS,
        minSize=(25, 25),
    )

    return largest_face, eyes


def are_eyes_open(eyes):
    return len(eyes) >= 2