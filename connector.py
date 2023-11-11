from datetime import datetime
# from faces import face_id
from app import app, mysql
from flask import Flask, jsonify, flash, request
from flaskext.mysql import MySQL

def find_next(datetimes_str):

    datetimes = [i for i in datetimes_str.split(";")]

    if len(datetimes) == 1:
        return datetimes_str

    diff = 8

    for i in datetimes:
        dayofweek = i[0]
        if datetime.now().weekday() - dayofweek > 0:
            diff = min(diff, (datetime.now().weekday() - dayofweek))
        elif dayofweek - datetime.now().weekday() > 0:
            diff = min(diff, (dayofweek + 7) - datetime.now().weekday())
        else:
            if datetime.now() > i.split("(")[1][:8].strftime('%H:%M:%S'): # convert string to datetime
                continue
            else:
                diff = 0

    for i in datetimes:
        if diff == i[0]:
            return i

# Find Student Info From Face
@app.route('/login', methods=['GET'])
def login():
    try:
        conn = mysql.connect()
        cursor =conn.cursor()
        face = "F001"
        select = """SELECT A.student_id, A.name, A.email
                    FROM Student AS A 
                    LEFT JOIN Faces AS B ON A.student_id = B.student_id
                    WHERE B.face_id='%s' """ % (face)
        execute = cursor.execute(select)
        student_values = cursor.fetchall()
        student_id, student_name, student_email = student_values[0]

        # Insert Login Record
        insert =  "INSERT INTO LoginHistory (student_id, login_datetime, logout_datetime, duration) VALUES (%s, %s, %s, %s)"
        val = (student_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), None, None)
        cursor.execute(insert, val)
        conn.commit()

        response = {
            "student_id": student_id,
            "student_name": student_name,
            "student_email": student_email 
        }

        return jsonify(response)
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()    
    

    
# Check if class in an hour
@app.route('/check', methods=['GET'])
def check():
    try:
        conn = mysql.connect()
        cursor =conn.cursor()
        student_id = request.args.get('student_id')

        # Check student's courses
        select = """SELECT A.course_id                      
                    FROM CourseRegistered AS A                      
                    LEFT JOIN Classroom AS B                      
                    ON A.course_id = B.course_id                     
                    WHERE A.student_id = '%s' AND B.dayofweek = %s AND NOW() BETWEEN B.startdate AND B.enddate AND TIMESTAMPDIFF(MINUTE, B.starttime, NOW()) <= 60                      
                    ORDER BY B.dayofweek ASC, B.starttime ASC""" % (student_id, datetime.now().weekday())
        execute = cursor.execute(select)
        student_course_id = cursor.fetchone()

        print(student_id, student_course_id[0])

        select = """SELECT E.course_id, E.course_name, E.starttime, E.endtime, E.classroom_name, E.zoom_link, E.instructor_message, F.file_links
                    FROM (
                        SELECT A.course_id, A.course_name, B.starttime, B.endtime, B.classroom_name, A.zoom_link, A.instructor_message
                        FROM Courses A
                        JOIN Classroom B ON A.course_id = B.course_id
                        JOIN ZoomLinks C ON A.course_id = C.course_id
                        WHERE A.course_id = '%s'
                    ) AS E
                    LEFT JOIN (
                        SELECT D.course_id, GROUP_CONCAT(D.note_file SEPARATOR '; ') AS file_links
                        FROM CourseMaterials D
                        WHERE D.note_date = DATE(NOW())
                        GROUP BY D.course_id
                    ) AS F ON E.course_id = F.course_id""" % (student_course_id[0])
        execute = cursor.execute(select)
        result = cursor.fetchall()
        course_id, course_name, starttime, endtime, classroom_name, zoom_link, instructor_message, file_links = result[0]

        print(result[0])
        starttime = str(starttime)
        endtime = str(endtime)
        
        response = {
            'course_id': course_id,
            'course_name': course_name,
            'starttime': starttime,
            'endtime': endtime,
            'classroom_name': classroom_name,
            'zoom_link': zoom_link,
            'instructor_message': instructor_message,
            'file_links': file_links
        }
        if not result[0]:
            return None
        else:
            return jsonify(response)
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()    
    

@app.route('/timetable', methods=['GET'])
def timetable():
    try:
        conn = mysql.connect()
        cursor =conn.cursor()
        student_id = request.args.get('student_id')
        print(student_id)
        # Check student's courses
        select = """SELECT D.course_name, D.instructor_name, D.schedule, D.classroom_name 
                    FROM CourseRegistered AS A
                    LEFT JOIN (     
                        SELECT B.course_id, B.course_name, B.instructor_name,
                            GROUP_CONCAT(CONCAT(C.dayofweek, ' (', C.starttime, ' - ', C.endtime, ')') SEPARATOR '; ') AS schedule,
                            C.startdate, C.enddate, C.classroom_name  
                        FROM Courses AS B
                        LEFT JOIN Classroom AS C ON B.course_id = C.course_id
                        WHERE NOW() BETWEEN C.startdate AND C.enddate 
                        GROUP BY B.course_id, C.startdate, C.enddate, C.classroom_name
                    ) AS D ON A.course_id = D.course_id 
                    WHERE A.student_id = '%s'
                """ % (student_id)
        execute = cursor.execute(select)
        timetable = cursor.fetchall()

        print(timetable)

        response = {
            "total_courses" : len(timetable),
            "course_names" : [i[0] for i in timetable],
            "instructor_name" : [i[1] for i in timetable],
            "next_class" : [i[2] for i in timetable],
            "classroom_name" : [i[3] for i in timetable]
        }

        return response

    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@app.route('/detail', methods=['GET'])
def detail():
    try:
        conn = mysql.connect()
        cursor =conn.cursor()

        course_id = request.args.get('course_id')
        # Get Course Detail
        select = """SELECT A.course_name,
                        GROUP_CONCAT(CONCAT(B.dayofweek, ' (', B.starttime, ' - ', B.endtime, ')') SEPARATOR '; ') AS schedule,
                        GROUP_CONCAT(B.classroom_name SEPARATOR '; ') AS classroom_names,
                        A.instructor_name, A.instructor_email, A.zoom_link, A.course_message, D.note_files
                    FROM Courses A
                    LEFT JOIN Classroom B ON A.course_id = B.course_id
                    LEFT JOIN (
                        SELECT course_id,
                            GROUP_CONCAT(CONCAT(note_title, ':', note_file) SEPARATOR '; ') AS note_files
                        FROM CourseMaterials
                        GROUP BY course_id
                    ) AS D ON A.course_id = D.course_id
                    WHERE A.course_id = '%s'
                    GROUP BY A.course_id, A.course_name, A.instructor_name, A.instructor_email, A.zoom_link, A.course_message, D.note_files;
                """ % (course_id)
        execute = cursor.execute(select)
        course_detail = cursor.fetchall()

        course_detail = course_detail[0]
        response = {
            "course_name": course_detail[0],
            "course_schedule": course_detail[1],
            "classroom_name": course_detail[2],
            "instructor_name": course_detail[3],
            "instructor_email": course_detail[4],
            "zoom_link": course_detail[5],
            "course_message": course_detail[6],
            "notes": course_detail[7]
        }

        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@app.route('/logout', methods=['PUT'])
def logout():
    student_id = request.args.get('student_id')
    conn = mysql.connect()
    cursor =conn.cursor()
    # Logout Update Database
    update =  "UPDATE LoginHistory SET logout_datetime=%s WHERE student_id=%s AND logout_datetime IS NULL" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), student_id)
    cursor.execute(update)
    update =  "UPDATE LoginHistory SET duration = TIMESTAMPDIFF(SECOND, login_datetime, logout_datetime) WHERE student_id=%s;" % (student_id)
    cursor.execute(update)

    return ('', 200)

if __name__ == '__main__':
    app.run()