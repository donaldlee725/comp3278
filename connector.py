from datetime import datetime
from faces import face_id
from app import app, mysql
from flask import Flask, jsonify, flash, request
from flaskext.mysql import MySQL


# Find Student Info From Face
@app.route("/login", methods=['GET'])
def login():
    
    try:
        conn = mysql.connect()
        cursor =conn.cursor()

        face = face_id(0)

        if face != "Your face is not recognized":
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
                "login": "Successful",
                "student_id": student_id,
                "student_name": student_name,
                "student_email": student_email 
            }

            return jsonify(response)
        else:
            return {"login":"Failed"}
        
    except Exception as e:
        print(e)
        return {"login":"Failed"}
    finally:
        cursor.close() 
        conn.close()
    
@app.route("/login2", methods=['GET'])
def login2():
    
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        student_email = request.args.get('email')
        student_password = request.args.get('password')
        

        select = """ SELECT A.student_id, A.name, A.email
                        FROM Student AS A 
                        LEFT JOIN Faces AS B ON A.student_id = B.student_id
                        WHERE A.email='%s' AND A.password='%s'""" % (student_email, student_password)
        execute = cursor.execute(select)
        student_values = cursor.fetchall()
        
        print(student_email, student_password, student_values)
        student_id, student_name, student_email = student_values[0]

        # Insert Login Record
        insert =  "INSERT INTO LoginHistory (student_id, login_datetime, logout_datetime, duration) VALUES (%s, %s, %s, %s)"
        val = (student_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), None, None)
        cursor.execute(insert, val)
        conn.commit()

        response = {
            "login": "Successful",
            "student_id": student_id,
            "student_name": student_name,
            "student_email": student_email 
        }

        return jsonify(response)
        
    except Exception as e:
        print(e)
        return {"login":"Failed"}
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
                    WHERE A.student_id = '%s' AND B.dayofweek = %s AND NOW() BETWEEN B.startdate AND B.enddate AND ABS(TIMESTAMPDIFF(MINUTE, B.starttime, NOW())) <= 60                      
                    ORDER BY B.dayofweek ASC, B.starttime ASC""" % (student_id, datetime.now().weekday())
        execute = cursor.execute(select)
        student_course_id = cursor.fetchone()
        # print(student_course_id[0])

        if student_course_id is None:
            cursor.close() 
            conn.close()
            return jsonify({
                "message": "No class fetched"
            })

        select = """
                SELECT E.course_id, E.course_name, E.starttime, E.endtime, E.classroom_name, E.zoom_link, E.course_message, F.file_links, I.dept_id, I.course_id, I.name, I.email, I.office_location, I.title, I.office_hour_start, I.office_hour_end, I.office_hour_weekday, I.instructor_meesage
                FROM (
                    SELECT A.course_id, A.course_name, A.course_message, B.starttime, B.endtime, B.classroom_name, A.zoom_link
                    FROM Courses A
                    JOIN Classroom B ON A.course_id = B.course_id
                    WHERE A.course_id = '%s'
                ) AS E
                LEFT JOIN (
                    SELECT D.course_id, GROUP_CONCAT(D.note_file SEPARATOR '; ') AS file_links
                    FROM CourseMaterials D
                    WHERE D.note_date = DATE(NOW())
                    GROUP BY D.course_id
                ) AS F ON E.course_id = F.course_id
                LEFT JOIN (
                    SELECT *
                    FROM Instructor I
                ) AS 
                """ % (student_course_id[0])
        
        execute = cursor.execute(select)
        result = cursor.fetchall()
        course_id, course_name, starttime, endtime, classroom_name, zoom_link, course_message, file_links, course_id, name, email, \
            office_location, title, office_hour_start, office_hour_end, office_hour_weekday, instructor_meesage = result[0]

        starttime = str(starttime)
        endtime = str(endtime)
        
        response = {
            "message": "Fetch Success",
            'course_id': course_id,
            'course_name': course_name,
            'course_message': course_message,
            'zoom_link': zoom_link,
            'starttime': starttime,
            'endtime': endtime,
            'classroom_name': classroom_name,
            'zoom_link': zoom_link,
            "course_message": course_message,
            'file_links': file_links,
            'instructor_name': name,
            'instructor_email': email,
            'office_location': office_location, 
            'title': title, 
            'office_hour_start': office_hour_start, 
            'office_hour_end': office_hour_end,
            'office_hour_weekday': office_hour_weekday,
            'instructor_meesage': instructor_meesage
        }

        return jsonify(response)
    except Exception as e:
        print(e)
        cursor.close() 
        conn.close()
        return jsonify({
            "message": "Fetch Failed"
        })
    

@app.route('/timetable', methods=['GET'])
def timetable():
    try:
        conn = mysql.connect()
        cursor =conn.cursor()
        student_id = request.args.get('student_id')
        print(student_id)
        # Check student's courses
        select = """SELECT A.course_id, D.course_name, D.instructor_name, D.schedule, D.classroom_name 
                    FROM CourseRegistered AS A
                    LEFT JOIN (
                        SELECT B.course_id, B.course_name, B.instructor_name,
                            GROUP_CONCAT(CONCAT(C.dayofweek, ' (', C.starttime, ' - ', C.endtime, ')') SEPARATOR '; ') AS schedule,
                            C.startdate, C.enddate, C.classroom_name  
                        FROM Courses AS B
                        LEFT JOIN Classroom AS C ON B.course_id = C.course_id
                        WHERE NOW() BETWEEN C.startdate AND C.enddate 
                        GROUP BY B.course_id, B.course_name, B.instructor_name, C.dayofweek, C.starttime, C.endtime, C.startdate, C.enddate, C.classroom_name
                        ORDER BY ABS(C.dayofweek - %s)
                    ) AS D ON A.course_id = D.course_id 
                    WHERE A.student_id = '%s'
                """ % (datetime.now().weekday(), student_id)
        execute = cursor.execute(select)
        timetable = cursor.fetchall()

        response = {
            "total_courses" : len(timetable),
            "course_names" : [i[1] for i in timetable],
            "instructor_name" : [i[2] for i in timetable],
            "next_class" : [i[3] for i in timetable],
            "classroom_name" : [i[4] for i in timetable]
        }

        return jsonify(response)

    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@app.route('/courses', methods=['GET'])
def courses():
    try:
        conn = mysql.connect()
        cursor =conn.cursor()
        student_id = request.args.get('student_id')
        # print(student_id)
        # Check student's courses
        select = """SELECT DISTINCT A.course_id, B.course_name, C.schedule, C.classrooms, E.title, E.name, F.dept_name
                    FROM CourseRegistered AS A
                    LEFT JOIN (
                        SELECT course_id, course_name, instructor_id, dept_id
                        FROM Courses
                    ) AS B ON A.course_id = B.course_id
                    LEFT JOIN (
                        SELECT C.course_id, GROUP_CONCAT(CONCAT(C.dayofweek, ' (', C.starttime, '-', C.endtime, ')') SEPARATOR ';') AS schedule,
                        GROUP_CONCAT(C.classroom_name SEPARATOR '; ') AS classrooms
                        FROM Classroom AS C
                        GROUP BY C.course_id
                    ) AS C ON B.course_id = C.course_id
                    LEFT JOIN (
                        SELECT D.course_id, D.startdate, D.enddate 
                        FROM Classroom AS D
                    ) AS D ON B.course_id = D.course_id
                    LEFT JOIN ( 
                        SELECT * FROM Instructor
                    ) AS E ON B.instructor_id = E.instructor_id
                    LEFT JOIN (
                        SELECT * FROM Department
                    ) AS F ON B.dept_id = F.dept_id 
                    WHERE NOW() BETWEEN D.startdate AND D.enddate AND A.student_id = '%s';
                """ % (student_id)
        execute = cursor.execute(select)
        timetable = cursor.fetchall()

        # print(timetable)

        response = {"message": "Fetch Success",
                    "total_courses": len(timetable),
                    "course_ids": [i[0] for i in timetable],
                    "course_names": [i[1] for i in timetable],
                    "course_schedules": [i[2] for i in timetable],
                    "classroom_names": [i[3] for i in timetable],
                    "instructor_titles": [i[4] for i in timetable],
                    "instructor_names": [i[5] for i in timetable],
                    "departments": [i[6] for i in timetable]}

        return jsonify(response)

    except Exception as e:
        return jsonify({
            "message": "Fetch Failed"
        })
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
                        GROUP_CONCAT(CONCAT(B.dayofweek, ' (', B.starttime, '-', B.endtime, ')') SEPARATOR ';') AS schedule,
                        GROUP_CONCAT(B.classroom_name SEPARATOR '; ') AS classroom_names,
                        E.name, E.email, E.office_location, E.title, E.office_hour_start, 
                        E.office_hour_end, E.office_hour_weekday, E.instructor_message, F.dept_name, A.zoom_link, A.course_message, D.note_files
                    FROM Courses A
                    LEFT JOIN Classroom B ON A.course_id = B.course_id
                    LEFT JOIN (
                        SELECT course_id,
                            GROUP_CONCAT(CONCAT(note_title, '|', note_file) SEPARATOR ';') AS note_files
                        FROM CourseMaterials
                        GROUP BY course_id
                    ) AS D ON A.course_id = D.course_id
                    LEFT JOIN (
                    SELECT *
                    FROM Instructor I
                    ) AS E ON A.instructor_id = E.instructor_id
                    LEFT JOIN ( 
                    SELECT *
                    FROM Department 
                    ) AS F ON A.dept_id = F.dept_id
                    WHERE A.course_id = '%s';
                """ % (course_id)
        execute = cursor.execute(select)
        course_detail = cursor.fetchall()

        course_detail = course_detail[0]
        response = {
            "message": "Fetch Success",
            "course_name": course_detail[0],
            "course_schedule": course_detail[1],
            "classroom_name": course_detail[2],
            "instructor_name": course_detail[3],
            "instructor_email": course_detail[4],
            "instructor_office_location": course_detail[5],
            "instructor_title": course_detail[6],
            "instructor_office_starttime": course_detail[7],
            "instructor_office_endtime": course_detail[8],
            "instructor_office_weekday": course_detail[9],
            "instructor_message": course_detail[10],
            "department": course_detail[11],
            "zoom_link": course_detail[12],
            "course_message": course_detail[13],
            "note_files": course_detail[14]
        }

        return jsonify(response)
    except Exception as e:
        return 
    finally:
        cursor.close() 
        conn.close()

@app.route('/logout', methods=['POST'])
def logout():
    student_id = request.args.get('student_id')
    conn = mysql.connect()
    cursor =conn.cursor()
    # Logout Update Database
    update =  "UPDATE LoginHistory SET logout_datetime = NOW() WHERE LoginHistory.student_id = '%s' AND LoginHistory.logout_datetime IS NULL" % (student_id)
    cursor.execute(update)
    conn.commit()
    update =  "UPDATE LoginHistory SET duration = TIMESTAMPDIFF(SECOND, login_datetime, logout_datetime) WHERE student_id='%s'" % (student_id)
    cursor.execute(update)
    conn.commit()

    return ('', 200)

if __name__ == '__main__':
    app.run()