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
            print(student_values)
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
        print(student_course_id)

        if student_course_id == None:
            cursor.close() 
            conn.close()
            return jsonify({
                "message": "No Data Fatched"
            })

        select = """
                SELECT A.course_id, A.course_name, A.course_message, A.zoom_link, B.starttime, B.endtime, B.classroom_name, C.file_links, I.dept_id, I.name, I.email, I.office_location, I.title, I.office_hour_start, I.office_hour_end, I.office_hour_weekday, I.instructor_message
                FROM (
                    SELECT A.course_id, A.course_name, A.course_message, A.zoom_link, A.instructor_id
                    FROM Courses AS A
                    WHERE A.course_id = '%s'
                ) AS A
                LEFT JOIN (
                    SELECT B.course_id,  B.starttime, B.endtime, B.classroom_name
                    FROM Classroom AS B
                    WHERE B.course_id = '%s' AND B.dayofweek = %s AND NOW() BETWEEN B.startdate AND B.enddate AND ABS(TIMESTAMPDIFF(MINUTE, B.starttime, NOW())) <= 60
                ) AS B ON A.course_id = B.course_id
                LEFT JOIN(
                    SELECT C.course_id, GROUP_CONCAT(C.note_file SEPARATOR '; ') AS file_links
                    FROM CourseMaterials AS C
                    WHERE C.note_date = DATE(NOW())
                    GROUP BY C.course_id
                ) AS C ON B.course_id = C.course_id
                LEFT JOIN (
                    SELECT *
                    FROM Instructor I
                ) AS I ON A.instructor_id = I.instructor_id
                """ % (student_course_id[0], student_course_id[0], datetime.now().weekday())

        execute = cursor.execute(select)
        result = cursor.fetchall()
        print(result)
        course_id, course_name, course_message, zoom_link, starttime, endtime, classroom_name, file_links, dept_id, \
            name, email, office_location, title, office_hour_start, office_hour_end, office_hour_weekday, instructor_message= result[0]

        starttime = str(starttime)
        endtime = str(endtime)
        
        response = {
            'course_id': course_id,
            'course_name': course_name,
            'course_message': course_message,
            'zoom_link': zoom_link,
            'starttime': starttime,
            'endtime': endtime,
            'classroom_name': classroom_name,
            'file_links': file_links,
            'name': name,
            'email': email,
            'office_location': office_location,
            'title': title,
            'office_hour_start': office_hour_start,
            'office_hour_end': office_hour_end,
            'office_hour_weekday': office_hour_weekday,
            'instructor_message': instructor_message
        }

        return jsonify(response)
    except Exception as e:
        print(e)
        cursor.close() 
        conn.close()
        return jsonify({
            "message": "%s Error" %(e)
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

        print(timetable)

        present_courses = set()
        final_timetable = []

        for row in timetable:
            if row[0] not in present_courses:
                present_courses.add(row[0])
                final_timetable.append(row) 

        response = {
            "total_courses" : len(final_timetable),
            "course_names" : [i[1] for i in final_timetable],
            "instructor_name" : [i[2] for i in final_timetable],
            "next_class" : [i[3] for i in final_timetable],
            "classroom_name" : [i[4] for i in final_timetable]
        }

        return jsonify(response)

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

        return jsonify(response)
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