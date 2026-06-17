-- Create the database
CREATE DATABASE college_db;
USE college_db;

-- 1. Departments table
CREATE TABLE departments (
    department_id INT PRIMARY KEY AUTO_INCREMENT,
    dept_name VARCHAR(100) NOT NULL,
    hod_name VARCHAR(100),
    budget DECIMAL(12,2)
);

-- 2. Students table
CREATE TABLE students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    date_of_birth DATE,
    department_id INT,
    enrollment_year INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- 3. Courses table
CREATE TABLE courses (
    course_id INT PRIMARY KEY AUTO_INCREMENT,
    course_name VARCHAR(150) NOT NULL,
    course_code VARCHAR(20) UNIQUE,
    credits INT,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- 4. Professors table
CREATE TABLE professors (
    professor_id INT PRIMARY KEY AUTO_INCREMENT,
    prof_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    department_id INT,
    salary DECIMAL(10,2),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- 5. Enrollments table
CREATE TABLE enrollments (
    enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    course_id INT,
    enrollment_date DATE,
    grade CHAR(2),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- ----------------
-- 	SAMPLE DATA
-- ----------------

-- Departments
INSERT INTO departments (dept_name, hod_name, budget) VALUES
('Computer Science', 'Dr. Ramesh Kumar', 850000.00),
('Electronics', 'Dr. Priya Nair', 620000.00),
('Mechanical', 'Dr. Suresh Iyer', 540000.00),
('Civil', 'Dr. Ananya Sharma', 430000.00);

-- Students
INSERT INTO students (first_name, last_name, email, date_of_birth, department_id, enrollment_year) VALUES
('Arjun', 'Mehta', 'arjun.mehta@college.edu', '2003-04-12', 1, 2022),
('Priya', 'Suresh', 'priya.suresh@college.edu', '2003-07-25', 1, 2022),
('Rohan', 'Verma', 'rohan.verma@college.edu', '2002-11-08', 2, 2021),
('Sneha', 'Patel', 'sneha.patel@college.edu', '2004-01-30', 3, 2023),
('Vikram', 'Das', 'vikram.das@college.edu', '2003-09-14', 1, 2022),
('Kavya', 'Menon', 'kavya.menon@college.edu', '2002-05-17', 2, 2021),
('Aditya', 'Singh', 'aditya.singh@college.edu', '2004-03-22', 4, 2023),
('Deepika', 'Rao', 'deepika.rao@college.edu', '2003-08-09', 1, 2022);

-- Courses
INSERT INTO courses (course_name, course_code, credits, department_id) VALUES
('Data Structures & Algorithms', 'CS101', 4, 1),
('Database Management Systems', 'CS102', 3, 1),
('Object Oriented Programming', 'CS103', 4, 1),
('Circuit Theory', 'EC101', 3, 2),
('Thermodynamics', 'ME101', 3, 3);

-- Enrollments
INSERT INTO enrollments (student_id, course_id, enrollment_date, grade) VALUES
(1, 1, '2022-07-01', 'A'), (1, 2, '2022-07-01', 'B'),
(2, 1, '2022-07-01', 'B'), (2, 3, '2022-07-01', 'A'),
(3, 1, '2021-07-01', 'A'), (4, 5, '2023-07-01', NULL),
(5, 1, '2022-07-01', 'C'), (5, 2, '2022-07-01', 'A'),
(6, 1, '2021-07-01', 'B'), (7, 5, '2023-07-01', NULL),
(8, 1, '2022-07-01', 'A'), (8, 3, '2022-07-01', 'B');

-- Professors
INSERT INTO professors (prof_name, email, department_id, salary) VALUES
('Dr. Anand Krishnan', 'anand.k@college.edu', 1, 95000.00),
('Dr. Meena Pillai', 'meena.p@college.edu', 2, 88000.00),
('Dr. Sunil Rajan', 'sunil.r@college.edu', 3, 82000.00),
('Dr. Kartik Gopal', 'kartik.g@college.edu', 4, 79000.00),
('Dr. Ramesh Babu', 'ramesh.b@college.edu', 1, 120000.00);

-- ==========================================
-- TASK 2: NORMALIZATION VERIFICATION
-- ==========================================

-- 1NF (First Normal Form):
-- All tables contain atomic (single-valued) attributes.
-- No column stores multiple values, repeating groups, or arrays.
-- Example violation: storing multiple phone numbers in one column
-- such as '9876543210,9988776655' would break 1NF.

-- 2NF (Second Normal Form):
-- All tables are in 1NF and every non-key attribute is fully
-- dependent on the whole primary key.
-- Most tables use a single-column primary key, so partial
-- dependency cannot occur.
-- In enrollments, the candidate key (student_id, course_id)
-- uniquely identifies a student's enrollment in a course.
-- enrollment_date and grade depend on the complete enrollment
-- relationship, not only on student_id or course_id.

-- 3NF (Third Normal Form):
-- All tables are in 2NF and contain no transitive dependencies.
-- Non-key attributes depend only on the primary key.
-- Department information (dept_name, hod_name, budget) is stored
-- only in departments and referenced through department_id.
-- Storing dept_name directly in students or professors would
-- create a transitive dependency and violate 3NF.

-- 3NF Analysis for Enrollments Table:
-- Primary Key: enrollment_id
-- Candidate Key: (student_id, course_id)
-- grade and enrollment_date depend directly on the enrollment record.
-- No non-key attribute determines another non-key attribute.
-- Therefore, the enrollments table satisfies 3NF.

-- 3NF Analysis for Departments Table:
-- Primary Key: department_id
-- Candidate Key: dept_name
-- No non-key attribute depends on another non-key attribute.
-- Therefore, the departments table satisfies 3NF.

-- 3NF Analysis for Students Table:
-- Primary Key: student_id
-- Candidate Key: email
-- No non-key attribute depends on another non-key attribute.
-- department_id is a foreign key, not a non-key attribute.
-- Therefore, the students table satisfies 3NF.

-- 3NF Analysis for Courses Table:
-- Primary Key: course_id
-- Candidate Key: course_code
-- No non-key attribute depends on another non-key attribute.
-- department_id is a foreign key, not a non-key attribute.
-- Therefore, the courses table satisfies 3NF.

-- 3NF Analysis for Professors Table:
-- Primary Key: professor_id
-- Candidate Key: email
-- No non-key attribute depends on another non-key attribute.
-- department_id is a foreign key, not a non-key attribute.
-- Therefore, the professors table satisfies 3NF.

-- ==========================================
-- TASK 3: ALTER AND EXTEND THE SCHEMA
-- ==========================================

-- 1. Add phone_number column to students table
ALTER TABLE students ADD COLUMN phone_number VARCHAR(15);

DESCRIBE students;

-- 2. Add max_seats column to courses table
ALTER TABLE courses ADD COLUMN max_seats INT DEFAULT 60;

DESCRIBE courses;

-- 3. Add CHECK constraint on enrollments.grade
ALTER TABLE enrollments ADD CONSTRAINT chk_grade CHECK (grade IN ('A','B','C','D','F') OR grade IS NULL);

DESCRIBE enrollments;

-- 4. Rename hod_name to head_of_dept
ALTER TABLE departments CHANGE COLUMN hod_name head_of_dept VARCHAR(100);

DESCRIBE departments;

-- 5. Drop phone_number column (Schema Rollback)
ALTER TABLE students DROP COLUMN phone_number;

DESCRIBE students;