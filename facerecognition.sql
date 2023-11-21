-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Feb 17, 2020 at 09:41 PM
-- Server version: 5.7.28-0ubuntu0.18.04.4
-- PHP Version: 7.2.24-0ubuntu0.18.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: facerecognition
--

-- --------------------------------------------------------

--
-- Table structure for table Student
--

DROP TABLE IF EXISTS LoginHistory;
DROP TABLE IF EXISTS CourseMaterials;
DROP TABLE IF EXISTS CourseRegistered;
DROP TABLE IF EXISTS Courses;
DROP TABLE IF EXISTS Classroom;
DROP TABLE IF EXISTS Faces;
DROP TABLE IF EXISTS Instructor;
DROP TABLE IF EXISTS Department;
DROP TABLE IF EXISTS Student;


CREATE TABLE Student (
  `student_id` VARCHAR(255) NOT NULL, 
  `name` VARCHAR(255) NOT NULL, 
  `email` VARCHAR(255) NOT NULL,
  PRIMARY KEY (student_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE Department (
  `dept_id` VARCHAR(10) NOT NULL,
  `dept_name` VARCHAR(50) NOT NULL,
  PRIMARY KEY(dept_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE Instructor (
  `dept_id` VARCHAR(10) NOT NULL,
  `instructor_id` VARCHAR(255) NOT NULL, 
  `name` VARCHAR(255) NOT NULL, 
  `email` VARCHAR(255) NOT NULL,
  `office_location` VARCHAR(30) NOT NULL,
  `title` VARCHAR(5) NOT NULL,
  `office_hour_start` DATETIME(3) NOT NULL,
  `office_hour_end` DATETIME(3) NOT NULL,
  `office_hour_weekday` VARCHAR(10) NOT NULL,
  `instructor_message` VARCHAR(255) NOT NULL,
  PRIMARY KEY (instructor_id),
  FOREIGN KEY (dept_id) REFERENCES Department(dept_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE Faces (
  `student_id` VARCHAR(255) NOT NULL,
  `face_id` VARCHAR(255) NOT NULL,
  FOREIGN KEY (student_id) REFERENCES Student(student_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE LoginHistory (
  `student_id` VARCHAR(255) NOT NULL,
  `login_datetime` DATETIME(3) NOT NULL,
  `logout_datetime` DATETIME(3),
  `duration` INT,
  FOREIGN KEY (student_id) REFERENCES Student(student_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE Courses (
  `course_id` VARCHAR(255) NOT NULL, 
  `course_name` VARCHAR(255) NOT NULL, 
  `course_message` VARCHAR(255),
  `dept_id` VARCHAR(10) NOT NULL,
  `zoom_link` VARCHAR(255),
  `instructor_id` VARCHAR(255) NOT NULL, 
  PRIMARY KEY (course_id),
  FOREIGN KEY (dept_id) REFERENCES Department(dept_id),
  FOREIGN KEY (instructor_id) REFERENCES Instructor(instructor_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE CourseRegistered (
  `registration_id` VARCHAR(255) NOT NULL, 
  `student_id` VARCHAR(255) NOT NULL, 
  `course_id` VARCHAR(255) NOT NULL,
  FOREIGN KEY (student_id) REFERENCES Student(student_id),
  FOREIGN KEY (course_id) REFERENCES Courses(course_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE CourseMaterials (
  `material_id` VARCHAR(10) NOT NULL,
  `course_id` VARCHAR(255) NOT NULL,
  `note_title` VARCHAR(255) NOT NULL,
  `note_file` VARCHAR(255),
  `note_date` DATE NOT NULL,
  PRIMARY KEY (material_id),
  FOREIGN KEY (course_id) REFERENCES Courses(course_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE Classroom (
  `classroom_id` VARCHAR(255) NOT NULL, 
  `classroom_name` VARCHAR(255) NOT NULL, 
  `course_id` VARCHAR(255) NOT NULL, 
  `startdate` DATE NOT NULL, 
  `enddate` DATE NOT NULL,
  `dayofweek` int NOT NULL, 
  `starttime` TIME NOT NULL,
  `endtime` TIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

-- Insert data into the Student table
INSERT INTO Student (student_id, name, email)
VALUES
    ('S001', 'John Doe', 'john@connect.hku.hk'),
    ('S002', 'Jane Smith', 'jane@connect.hku.hk'),
    ('S003', 'David Lee', 'david@connect.hku.hk'),
    ('S004', 'Emily Wang', 'emily@connect.hku.hk'),
    ('S005', 'Michael Liu', 'michael@connect.hku.hk');

-- Insert data into the Department table
INSERT INTO Department (dept_id, dept_name)
VALUES
    ('D001', 'Computer Science'),
    ('D002', 'Mathematics'),
    ('D003', 'Economics'),
    ('D004', 'Psychology'),
    ('D005', 'Physics');

-- Insert data into the Instructor table
INSERT INTO Instructor (dept_id, instructor_id, name, email, office_location, title, office_hour_start, office_hour_end, office_hour_weekday, instructor_message)
VALUES
    ('D001', 'I001', 'Ping Luo', 'pluo@cs.hku.hk', 'CB326', 'Prof.', '2023-11-20 09:00:00', '2023-11-20 11:00:00', 0, 'Welcome to the course!'),
    ('D001', 'I002', 'Emma Johnson', 'emmajohnson@hku.hk', 'Building B, Room 201', 'Prof.', '2023-11-20 14:00:00', '2023-11-20 16:00:00', 2, 'Don''t forget to submit assignments!'),
    ('D001', 'I003', 'David Chen', 'davidchen@hku.hk', 'Building C, Room 305', 'Dr.', '2023-11-20 10:30:00', '2023-11-20 12:30:00', 1, 'Office hours canceled on November 30th.'),
    ('D002', 'I004', 'Lisa Wang', 'lisawang@hku.hk', 'Building D, Room 501', 'Prof.', '2023-11-20 13:00:00', '2023-11-20 15:00:00', 3, 'Feel free to ask questions!'),
    ('D003', 'I005', 'Michael Liu', 'michael.liu@hku.hk', 'Building E, Room 401', 'Dr.', '2023-11-20 16:30:00', '2023-11-20 18:30:00', 4, 'Reminder: Midterm exam next week.'),
    ('D004', 'I006', 'Michel Wang', 'michelwang@hku.hk', 'Building F, Room 403', 'Dr.', '2023-11-20 13:30:00', '2023-11-20 15:30:00', 4, 'Reminder: Midterm exam cancelled.'),
    ('D005', 'I007', 'Eren Chan', 'erenchan@hku.hk', 'Building G, Room 205', 'Dr.', '2023-11-20 11:30:00', '2023-11-20 13:30:00', 4, NULL);   

-- Insert data into the Faces table
INSERT INTO Faces (student_id, face_id)
VALUES
    ('S001', 'F001'),
    ('S002', 'F002'),
    ('S003', 'F003'),
    ('S004', 'F004'),
    ('S005', 'F005');

-- Insert data into the LoginHistory table
INSERT INTO LoginHistory (student_id, login_datetime, logout_datetime, duration)
VALUES
    ('S001', '2023-11-19 09:00:00', '2023-11-19 10:30:00', 10),
    ('S002', '2023-11-19 13:45:00', '2023-11-19 15:00:00', 15),
    ('S003', '2023-11-19 10:30:00', '2023-11-19 11:00:00', 5),
    ('S004', '2023-11-19 14:00:00', '2023-11-19 16:30:00', 3),
    ('S005', '2023-11-19 16:00:00', '2023-11-19 17:30:00', 8);

-- Insert data into the Courses table
INSERT INTO Courses (course_id, course_name, course_message, dept_id, zoom_link, instructor_id)
VALUES
    ('COMP3278', 'Introduction to Database Management Systems', 'Welcome to the course!', 'D001', 'zoom.us/join/C001', 'I001'),
    ('COMP3331', 'Machine Learning', 'Don''t forget to submit assignments!', 'D001', 'zoom.us/join/C003', 'I002'),
    ('COMP3297', 'Software Engineering', 'Welcome!', 'D001', 'zoom.us/join/C003', 'I003'),
    ('MATH2014', 'Multivariable Calculus', 'Feel free to ask questions!', 'D002', 'zoom.us/join/C004', 'I004'),
    ('ECON1280', 'Analysis of Economic Data', 'Reminder: Midterm exam next week.', 'D003', 'zoom.us/join/C005', 'I005'),
    ('PSYC1001', 'Introduction to Psychology', 'next week come to class', 'D004', 'zoom.us/join/C006', 'I006'),
    ('PHYS1250', 'Fundamental Physics', 'Don''t forget to submit assignments', 'D005', 'zoom.us/join/C007', 'I007');

-- Insert data into the CourseRegistered table
INSERT INTO CourseRegistered (registration_id, student_id, course_id)
VALUES
    ('R001', 'S001', 'COMP3278'),
    ('R002', 'S001', 'COMP3331'),
    ('R003', 'S001', 'MATH2014'),
    ('R004', 'S001', 'ECON1280'),
    ('R005', 'S002', 'COMP3297'),
    ('R006', 'S002', 'PSYC1001'),
    ('R007', 'S002', 'PHYS1250'),
    ('R008', 'S002', 'COMP3278'),
    ('R009', 'S003', 'COMP3331'),
    ('R010', 'S003', 'PSYC1001'),
    ('R011', 'S003', 'COMP3297'),
    ('R012', 'S003', 'MATH2014'),
    ('R013', 'S004', 'ECON1280'),
    ('R014', 'S004', 'COMP3278'),
    ('R015', 'S004', 'PHYS1250'),
    ('R016', 'S004', 'COMP3297'),
    ('R017', 'S005', 'COMP3331'),
    ('R018', 'S005', 'PHYS1250'),
    ('R019', 'S005', 'ECON1280'),
    ('R020', 'S005', 'COMP3278');

-- For Course ID: COMP3278
INSERT INTO CourseMaterials (material_id, course_id, note_title, note_file, note_date)
VALUES
    ('M001', 'COMP3278', 'ER model', 'https://moodle.hku.hk/mod/resource/view.php?id=3081960', '2023-10-01'),
    ('M002', 'COMP3278', 'ER design', 'https://moodle.hku.hk/mod/resource/view.php?id=3095373', '2023-10-07'),
    ('M003', 'COMP3278', 'SQL basic', 'https://moodle.hku.hk/mod/resource/view.php?id=3095391', '2023-10-20'),
    ('M004', 'COMP3278', 'Relational Algebra', 'https://moodle.hku.hk/mod/resource/view.php?id=3133990', '2023-11-01'),
    ('M005', 'COMP3278', 'Functional Dependence', 'https://moodle.hku.hk/mod/resource/view.php?id=3154202', '2023-11-20');

-- For Course ID: COMP3331
INSERT INTO CourseMaterials (material_id, course_id, note_title, note_file, note_date)
VALUES
    ('M006', 'COMP3331', 'Introduction to Machine Learning', 'intro_ml.pdf', '2023-09-01'),
    ('M007', 'COMP3331', 'Supervised Learning Techniques', 'supervised_learning.pdf', '2023-09-05'),
    ('M008', 'COMP3331', 'Unsupervised Learning Methods', 'unsupervised_learning.pdf', '2023-09-10'),
    ('M009', 'COMP3331', 'Deep Learning Fundamentals', 'deep_learning.pdf', '2023-09-15'),
    ('M010', 'COMP3331', 'Machine Learning Project Guidelines', 'ml_project_guidelines.pdf', '2023-09-20');

-- For Course ID: COMP3297
INSERT INTO CourseMaterials (material_id, course_id, note_title, note_file, note_date)
VALUES
    ('M011', 'COMP3297', 'Introduction to Software Engineering', 'intro_se.pdf', '2023-09-01'),
    ('M012', 'COMP3297', 'Software Development Life Cycle', 'sdlc.pdf', '2023-09-05'),
    ('M013', 'COMP3297', 'Agile Methodologies', 'agile_methodologies.pdf', '2023-09-10'),
    ('M014', 'COMP3297', 'Software Testing Techniques', 'software_testing.pdf', '2023-09-15'),
    ('M015', 'COMP3297', 'Software Engineering Project Guidelines', 'se_project_guidelines.pdf', '2023-09-20');

-- For Course ID: MATH2014
INSERT INTO CourseMaterials (material_id, course_id, note_title, note_file, note_date)
VALUES
    ('M016', 'MATH2014', 'Introduction to Multivariable Calculus', 'intro_multivar_calc.pdf', '2023-09-01'),
    ('M017', 'MATH2014', 'Partial Derivatives', 'partial_derivatives.pdf', '2023-09-05'),
    ('M018', 'MATH2014', 'Double Integrals', 'double_integrals.pdf', '2023-09-10'),
    ('M019', 'MATH2014', 'Vector Calculus', 'vector_calculus.pdf', '2023-09-15'),
    ('M020', 'MATH2014', 'Applications of Multivariable Calculus', 'applications_multivar_calc.pdf', '2023-09-20');

-- For Course ID: ECON1280
INSERT INTO CourseMaterials (material_id, course_id, note_title, note_file, note_date)
VALUES
    ('M021', 'ECON1280', 'Introduction to Economic Data Analysis', 'intro_econ_data_analysis.pdf', '2023-09-01'),
    ('M022', 'ECON1280', 'Descriptive Statistics in Economics', 'descriptive_stats_economics.pdf', '2023-09-05'),
    ('M023', 'ECON1280', 'Regression Analysis', 'regression_analysis.pdf', '2023-09-10'),
    ('M024', 'ECON1280', 'Time Series Analysis', 'time_series_analysis.pdf', '2023-09-15'),
    ('M025', 'ECON1280', 'Hypothesis Testing in Economics', 'hypothesis_testing_economics.pdf', '2023-09-20');

-- For Course ID: PSYC1001
INSERT INTO CourseMaterials (material_id, course_id, note_title, note_file, note_date)
VALUES
    ('M026', 'PSYC1001', 'Introduction to Psychology', 'intro_psychology.pdf', '2023-09-01'),
    ('M027', 'PSYC1001', 'Cognitive Psychology', 'cognitive_psychology.pdf', '2023-09-05'),
    ('M028', 'PSYC1001', 'Social Psychology', 'social_psychology.pdf', '2023-09-10'),
    ('M029', 'PSYC1001', 'Abnormal Psychology', 'abnormal_psychology.pdf', '2023-09-15'),
    ('M030', 'PSYC1001', 'Research Methods in Psychology', 'research_methods_psychology.pdf', '2023-09-20');

-- Insert sample CourseMaterials data for PHYS1250
INSERT INTO CourseMaterials (material_id, course_id, note_title, note_file, note_date)
VALUES
    ('M031', 'PHYS1250', 'Introduction to Fundamental Physics', 'intro_fundamental_physics.pdf', '2023-09-01'),
    ('M032', 'PHYS1250', 'Newtonian Mechanics', 'newtonian_mechanics.pdf', '2023-09-05'),
    ('M033', 'PHYS1250', 'Electromagnetism', 'electromagnetism.pdf', '2023-09-10'),
    ('M034', 'PHYS1250', 'Quantum Mechanics', 'quantum_mechanics.pdf', '2023-09-15'),
    ('M035', 'PHYS1250', 'Modern Physics', 'modern_physics.pdf', '2023-09-20');

-- Insert data into the Classroom table
INSERT INTO Classroom (classroom_id, classroom_name, course_id, startdate, enddate, dayofweek, starttime, endtime)
VALUES
    ('C001', 'MWT 1', 'COMP3278', '2023-09-01', '2023-11-30', 0, '09:00:00', '10:00:00'),
    ('C002', 'MWT 2', 'COMP3331', '2023-09-01', '2023-11-30', 2, '09:00:00', '10:00:00'),
    ('C003', 'KK 201', 'COMP3297', '2023-09-01', '2023-11-30', 4, '09:00:00', '10:00:00'),
    ('C004', 'KK 202', 'MATH2014', '2023-09-01', '2023-11-30', 1, '09:00:00', '10:00:00'),
    ('C002', 'MWT 2', 'ECON1280', '2023-09-01', '2023-11-30', 3, '09:00:00', '10:00:00'),
    ('C005', 'KB 223', 'COMP3278', '2023-09-01', '2023-11-30', 0, '11:00:00', '12:00:00'),
    ('C006', 'CYPP 1', 'COMP3331', '2023-09-01', '2023-11-30', 1, '12:00:00', '13:00:00'),
    ('C007', 'CPD 1', 'COMP3297', '2023-09-01', '2023-11-30', 2, '11:00:00', '12:00:00'),
    ('C008', 'KK 301', 'MATH2014', '2023-09-01', '2023-11-30', 3, '12:00:00', '13:00:00'),
    ('C001', 'MWT 1', 'PHYS1250', '2023-09-01', '2023-11-30', 2, '11:00:00', '12:00:00'),
    ('C007', 'CPD 1', 'PHYS1250', '2023-09-01', '2023-11-30', 3, '12:00:00', '13:00:00'),
    ('C005', 'KB 223', 'PSYC1001', '2023-09-01', '2023-11-30', 0, '10:00:00', '11:00:00');