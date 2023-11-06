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
DROP TABLE IF EXISTS ZoomLinks;
DROP TABLE IF EXISTS CourseMaterials;
DROP TABLE IF EXISTS CourseRegistered;
DROP TABLE IF EXISTS Courses;
DROP TABLE IF EXISTS Classroom;
DROP TABLE IF EXISTS Student;


CREATE TABLE Student (
  `student_id` VARCHAR(255) NOT NULL, 
  `name` VARCHAR(255) NOT NULL, 
  `email` VARCHAR(255) NOT NULL,
  PRIMARY KEY (student_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES Student WRITE;
/*!40000 ALTER TABLE Student DISABLE KEYS */;
INSERT INTO Student VALUES (1, "Donald", "dlee725@connect.hku.hk");
/*!40000 ALTER TABLE Student ENABLE KEYS */;
UNLOCK TABLES;

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
  `instructor_message` VARCHAR(255),
  PRIMARY KEY (course_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE CourseRegistered (
  `registration_id` VARCHAR(255) NOT NULL, 
  `student_id` VARCHAR(255) NOT NULL, 
  `course_id` VARCHAR(255) NOT NULL,
  FOREIGN KEY (student_id) REFERENCES Student(student_id),
  FOREIGN KEY (course_id) REFERENCES Courses(course_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE ZoomLinks (
  `zoom_id` INT NOT NULL,
  `course_id` VARCHAR(255) NOT NULL,
  `zoom_link` VARCHAR(255) NOT NULL,
  `meeting_datetime` DATETIME(6) NOT NULL,
  PRIMARY KEY (zoom_id),
  FOREIGN KEY (course_id) REFERENCES Courses(course_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE CourseMaterials (
  `material_id` INT NOT NULL,
  `course_id` VARCHAR(255) NOT NULL,
  `note_title` VARCHAR(255) NOT NULL,
  `note_description` VARCHAR(255),
  `note_file` VARCHAR(255),
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
