import urllib
import numpy as np
import mysql.connector
import cv2
import pyttsx3
import pickle
from datetime import datetime
import sys

def face_id(conf):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("train.yml")

    labels = {"person_name": 1}
    path = "labels.pickle"
    with open(path, "rb") as f:
        labels = pickle.load(f)
        labels = {v: k for k, v in labels.items()}

    # Define camera and detect face
    face_cascade = cv2.CascadeClassifier(
        'haarcascade/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(1)

    # 3 Open the camera and start face recognition
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.5, minNeighbors=5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            # predict the id and confidence for faces
            id_, conf = recognizer.predict(roi_gray)

            # If the face is recognized
            if conf >= conf:
                font = cv2.QT_FONT_NORMAL
                id = 0
                id += 1
                student_face_id = labels[id_]
                color = (255, 0, 0)
                stroke = 2
                cv2.putText(frame, student_face_id, (x, y), font, 1,
                            color, stroke, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))
                return student_face_id
            else:
                color = (255, 0, 0)
                stroke = 2
                font = cv2.QT_FONT_NORMAL
                cv2.putText(frame, "UNKNOWN", (x, y), font,
                            1, color, stroke, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))
                return "Your face is not recognized"

        # cv2.imshow('Attendance System', frame)
        k = cv2.waitKey(20) & 0xff
        if k == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

                


