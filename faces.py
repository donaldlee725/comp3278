import urllib
import numpy as np
import mysql.connector
import cv2
import pyttsx3
import pickle
from datetime import datetime
import sys

# 1 Create database connection
myconn = mysql.connector.connect(host="localhost", user="root", passwd="725Donald725", database="facerecognition")
date = datetime.utcnow()
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
cursor = myconn.cursor()

in_cam = {}

#2 Load recognize and read label from model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("train.yml")

labels = {"person_name": 1}
with open("labels.pickle", "rb") as f:
    labels = pickle.load(f)
    labels = {v: k for k, v in labels.items()}

# create text to speech
engine = pyttsx3.init("dummy")
rate = engine.getProperty("rate")
engine.setProperty("rate", 175)

# Define camera and detect face
face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(1)

# 3 Open the camera and start face recognition
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

    # print(in_cam)
    for student_id in in_cam.copy():
        in_cam[student_id] -= 1
        if in_cam[student_id] == 0:
            update =  "UPDATE LoginHistory SET logout_datetime=%s WHERE student_id=%s AND logout_datetime IS NULL"
            val = (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), student_id)
            cursor.execute(update, val)
            update =  "UPDATE LoginHistory SET duration = TIMESTAMPDIFF(SECOND, login_datetime, logout_datetime);"
            cursor.execute(update)
            in_cam.pop(student_id)

    for (x, y, w, h) in faces:
        # print(x, w, y, h)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        id_, conf = recognizer.predict(roi_gray)

        # If the face is recognized
        if conf >= 1:
            font = cv2.QT_FONT_NORMAL
            student_id = labels[id_]

            # Find the student's information in the database.
            select = "SELECT student_id, name, email FROM Student WHERE name='%s'" % (student_id)
            execute = cursor.execute(select)
            result = cursor.fetchall()

            data = None
            try:
                student_id, student_name, student_email = result[0]
            except:
                data = "error"
            

            color = (255, 0, 0)
            stroke = 2
            cv2.putText(frame, student_name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))

            # If the student's information is found in the database
            if data == "error":
                print("The student", student_id, "is NOT FOUND in the database.")
            
            else:
                if student_id not in in_cam:
                    # Update the data in database
                    insert =  "INSERT INTO LoginHistory (student_id, login_datetime, logout_datetime, duration) VALUES (%s, %s, %s, %s)"
                    val = (result[0][0], datetime.now().strftime('%Y-%m-%d %H:%M:%S'), None, None)
                    cursor.execute(insert, val)
                    myconn.commit()
                
                    hello = ("Hello ", student_name, "You did attendance today")

                    # select = """SELECT B.course_id, B.course_name, C.classroom_id, C.classroom_name, 
                    #                 C.startdate, C.enddate, C.dayofweek, C.starttime, C.endtime
                    #             FROM CourseRegistered A
                    #             LEFT JOIN (
                    #                 SELECT Courses.course_id, Courses.course_name, Classroom.classroom_id, Classroom.classroom_name, 
                    #                     Classroom.startdate, Classroom.enddate, Classroom.dayofweek, Classroom.starttime, Classroom.endtime
                    #                 FROM Courses 
                    #                 LEFT JOIN Classroom ON Courses.course_id = Classroom.course_id
                    #             ) AS D ON A.course_id = D.course_id
                    #             WHERE A.student_id = %s AND %s BETWEEN D.startdate AND D.enddate
                    #             ORDER BY D.dayofweek ASC, D.starttime ASC;""" % (student_id, datetime.now().strftime('%Y-%m-%d'))
                    # execute = cursor.execute(select)
                    # result = cursor.fetchall()
                    
                    # for i in result[0]:
                    #     time_diff = ((datetime.now().strftime("%H:%M") - datetime.strptime(i[7], "%H:%M")) % 3600) // 60
                    #     if i[6] == date.weekday() and time_diff <= 60:
                            
                    #     else:
                    #         # display result

                in_cam[student_id] = 10

        # If the face is unrecognized
        else: 
            color = (255, 0, 0)
            stroke = 2
            font = cv2.QT_FONT_NORMAL
            cv2.putText(frame, "UNKNOWN", (x, y), font, 1, color, stroke, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))

    cv2.imshow('Attendance System', frame)

    k = cv2.waitKey(20) & 0xff
    if k == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()



