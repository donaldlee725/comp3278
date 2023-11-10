from datetime import datetime
from faces import face_id
from app import app, mysql
from flask import Flask, jsonify, flash, request
from flask_mysql import MySQL



# Find Student Info From Face
@app.route('/login', methods=['GET'])
def login():
    try:
        conn = mysql.connect()
        cursor =conn.cursor()
        face = face_id(20)
        select = """SELECT A.student_id, A.name, A.email
                    FROM Student AS A 
                    LEFT JOIN Faces AS B ON A.student_id = B.student_id
                    WHERE B.face_id=%s""" % (face)
        execute = cursor.execute(select)
        student_values = cursor.fetchall()
        student_id, student_name, student_email = student_values[0]

        # Insert Login Record
        insert =  "INSERT INTO LoginHistory (student_id, login_datetime, logout_datetime, duration) VALUES (%s, %s, %s, %s)"
        val = (student_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), None, None)
        cursor.execute(insert, val)
        conn.commit()

        return (student_values[0], 200)
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
                    LEFT JOIN Classroom AS B ON A.course_id = B.course_id
                    WHERE A.student_id = %s AND B.dayofweek = %s AND 
                    %s BETWEEN B.startdate AND B.enddate AND TIMESTAMPDIFF(MINUTE, B.starttime, NOW()) <= 60
                    ORDER BY D.dayofweek ASC, D.starttime ASC""" % (student_id, datetime.now().date())
        execute = cursor.execute(select)
        student_course_id = cursor.fetchone()


        select = """SELECT E.course_id, E.course_name, E.starttime, E.endtime, E.classroom_name, E.zoom_link, E.instructor_message, F.file_links
                    FROM (
                        SELECT A.course_id, A.course_name, B.starttime, B.endtime, B.classroom_name, C.zoom_link, A.instructor_message
                        FROM Courses A
                        JOIN Classroom B ON A.course_id = B.course_id
                        JOIN ZoomLinks C ON A.course_id = C.course_id
                        WHERE A.course_id = %s
                    ) AS E
                    LEFT JOIN (
                        SELECT D.course_id, GROUP_CONCAT(D.note_file SEPARATOR '; ') AS file_links
                        FROM CourseMaterials D
                        WHERE D.note_date = %s
                        GROUP BY D.course_id
                    ) AS F ON E.course_id = F.course_id""" % (student_course_id, datetime.now().date())
        execute = cursor.execute(select)
        result = cursor.fetchall()

        if not result:
            return ('', 204)
        else:
            return (result[0], 200)
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
        # Check student's courses
        select = """SELECT D.course_name, D.instructor_name, D.dayofweek, 
                    D.starttime, D.endtime, D.classroom_name
                    FROM CourseRegistered AS A
                    LEFT JOIN (
                        SELECT *
                        FROM Courses AS B
                        LEFT JOIN Classroom AS C ON B.course_id = C.course_id
                    ) AS D ON A.course_id = D.course_id
                    WHERE A.student_id = %s AND %s BETWEEN D.startdate AND D.enddate
                    ORDER BY D.dayofweek ASC, D.starttime ASC""" % (student_id, datetime.now().date())
        execute = cursor.execute(select)
        timetable = cursor.fetchall()

        return (timetable[0], 200)
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
                    A.instructor_name, A.instructor_email, C.zoom_link, A.course_message,
                    GROUP_CONCAT(CONCAT(D.note_title, ':', D.note_file) SEPARATOR '; ') AS note_files
                    FROM Courses A
                    LEFT JOIN Classroom B ON A.course_id = B.course_id
                    LEFT JOIN ZoomLinks C ON A.course_id = C.course_id
                    LEFT JOIN CourseMaterials D ON A.course_id = D.course_id
                    WHERE A.course_id = %s""" % (course_id)
        execute = cursor.execute(select)
        course_detail = cursor.fetchall()
        return (course_detail[0], 200)
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