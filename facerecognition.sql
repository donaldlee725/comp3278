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
DROP TABLE IF EXISTS Student;


CREATE TABLE Student (
  `student_id` VARCHAR(255) NOT NULL, 
  `name` VARCHAR(255) NOT NULL, 
  `email` VARCHAR(255) NOT NULL,
  PRIMARY KEY (student_id)
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
  `instructor_name` VARCHAR(255),
  `instructor_email` VARCHAR(255),
  `instructor_message` VARCHAR(255),
  `zoom_link` VARCHAR(255),
  PRIMARY KEY (course_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE CourseRegistered (
  `registration_id` VARCHAR(255) NOT NULL, 
  `student_id` VARCHAR(255) NOT NULL, 
  `course_id` VARCHAR(255) NOT NULL,
  FOREIGN KEY (student_id) REFERENCES Student(student_id),
  FOREIGN KEY (course_id) REFERENCES Courses(course_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE CourseMaterials (
  `material_id` INT NOT NULL,
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

-- Sample data for Student table
INSERT INTO Student (student_id, name, email)
VALUES ('S001', 'John Doe', 'john.doe@example.com'),
       ('S002', 'Jane Smith', 'jane.smith@example.com'),
       ('S003', 'Michael Johnson', 'michael.johnson@example.com');

-- Sample data for Faces table
INSERT INTO Faces (face_id, student_id)
VALUES ('F001', 'S001'),
       ('F002', 'S002'),
       ('F003', 'S003');

-- Sample data for LoginHistory table
INSERT INTO LoginHistory (student_id, login_datetime, logout_datetime, duration)
VALUES ('S001', '2023-11-10 09:00:00', '2023-11-10 10:30:00', 90),
       ('S002', '2023-11-10 11:00:00', '2023-11-10 12:30:00', 90),
       ('S003', '2023-11-10 13:00:00', '2023-11-10 14:30:00', 90);

-- Sample data for Courses table
INSERT INTO Courses (course_id, course_name, course_message, instructor_name, instructor_email, instructor_message)
VALUES ('C001', 'Mathematics', 'Welcome to the Mathematics course!', 'Prof. Smith', 'smith@example.com', 'Please review the syllabus.'),
       ('C002', 'English Literature', 'Welcome to the English Literature course!', 'Prof. Johnson', 'johnson@example.com', 'Please bring your textbooks.');

-- Sample data for CourseRegistered table
INSERT INTO CourseRegistered (registration_id, student_id, course_id)
VALUES ('R001', 'S001', 'C001'),
       ('R002', 'S002', 'C001'),
       ('R003', 'S001', 'C002');
       
-- Sample data for CourseMaterials table
INSERT INTO CourseMaterials (material_id, course_id, note_title, note_file, note_date)
VALUES (1, 'C001', 'Lecture 1', 'lecture1.pdf', '2023-11-11'),
       (2, 'C001', 'Lecture 2', 'lecture2.pdf', '2023-11-11'),
       (3, 'C002', 'Introduction', 'intro.pdf', '2023-11-02');

INSERT INTO Classroom (classroom_id, classroom_name, course_id, startdate, enddate, dayofweek, starttime, endtime)
VALUES ('CL001', 'Room 101', 'C001', '2023-11-01', '2024-01-15', 4, '15:00:00', '17:00:00'),
       ('CL002', 'Room 102', 'C001', '2023-11-01', '2024-01-15', 2, '13:00:00', '15:00:00'),
       ('CL002', 'Room 102', 'C002', '2023-11-01', '2024-01-20', 3, '14:00:00', '16:00:00');