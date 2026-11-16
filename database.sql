-- Placement Tracker System - MySQL schema
DROP DATABASE IF EXISTS placement;
CREATE DATABASE placement;
USE placement;

-- Admin users
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);

-- Default admin (change this after first login setup)
INSERT INTO users (email, password) VALUES ('admin@example.com', 'admin123');

-- Student registrations / profiles
CREATE TABLE placement_registration (
    student_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100),
    phone VARCHAR(15),
    department VARCHAR(50),
    graduation_year INT,
    company VARCHAR(255),
    status VARCHAR(20),
    package VARCHAR(100),
    role VARCHAR(100),
    timing VARCHAR(100)
);

-- Placement drives
CREATE TABLE drives (
    drive_id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(100),
    drive_date DATE,
    location VARCHAR(100),
    package_details VARCHAR(100),
    eligibility VARCHAR(255),
    description TEXT
);

-- Student <-> drive registrations
CREATE TABLE registrations (
    reg_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(20),
    drive_id INT,
    status VARCHAR(20),
    notes TEXT,
    registration_date DATETIME,
    FOREIGN KEY (student_id) REFERENCES placement_registration(student_id),
    FOREIGN KEY (drive_id) REFERENCES drives(drive_id)
);
