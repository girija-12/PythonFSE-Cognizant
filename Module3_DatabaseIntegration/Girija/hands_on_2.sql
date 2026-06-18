USE college_db;

-- TASK 1: INSERT, UPDATE AND DELETE DATA

-- Departments
INSERT INTO departments (dept_name, hod_name, budget) VALUES
('Computer Science', 'Dr. Ramesh Kumar', 850000.00),
('Electronics', 'Dr. Priya Nair', 620000.00),
('Mechanical', 'Dr. Suresh Iyer', 540000.00),
('Civil', 'Dr. Ananya Sharma', 430000.00);
SELECT COUNT(*) FROM departments;

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

INSERT INTO students (first_name, last_name, email, date_of_birth, department_id, enrollment_year) VALUES
('Aswathi', 'AJ', 'aswathi.aj@rit.edu', '2006-03-23',1,2023),
('Girija','R', 'girija.r@rit.edu', '2006-01-12', 1, 2023);
SELECT COUNT(*) FROM students;

-- Courses
INSERT INTO courses (course_name, course_code, credits, department_id) VALUES
('Data Structures & Algorithms', 'CS101', 4, 1),
('Database Management Systems', 'CS102', 3, 1),
('Object Oriented Programming', 'CS103', 4, 1),
('Circuit Theory', 'EC101', 3, 2),
('Thermodynamics', 'ME101', 3, 3);
SELECT COUNT(*) FROM courses;

-- Enrollments
INSERT INTO enrollments (student_id, course_id, enrollment_date, grade) VALUES
(1, 1, '2022-07-01', 'A'), (1, 2, '2022-07-01', 'B'),
(2, 1, '2022-07-01', 'B'), (2, 3, '2022-07-01', 'A'),
(3, 1, '2021-07-01', 'A'), (4, 5, '2023-07-01', NULL),
(5, 1, '2022-07-01', 'C'), (5, 2, '2022-07-01', 'A'),
(6, 1, '2021-07-01', 'B'), (7, 5, '2023-07-01', NULL),
(8, 1, '2022-07-01', 'A'), (8, 3, '2022-07-01', 'B');
SELECT COUNT(*) FROM enrollments;

-- Professors
INSERT INTO professors (prof_name, email, department_id, salary) VALUES
('Dr. Anand Krishnan', 'anand.k@college.edu', 1, 95000.00),
('Dr. Meena Pillai', 'meena.p@college.edu', 2, 88000.00),
('Dr. Sunil Rajan', 'sunil.r@college.edu', 3, 82000.00),
('Dr. Kartik Gopal', 'kartik.g@college.edu', 4, 79000.00),
('Dr. Ramesh Babu', 'ramesh.b@college.edu', 1, 120000.00);
SELECT COUNT(*) FROM professors;

UPDATE enrollments SET grade='B' WHERE student_id=5 and course_id=1;
SELECT COUNT(*) FROM enrollments;

DELETE FROM enrollments WHERE grade IS NULL AND enrollment_id>0;
SELECT COUNT(*) FROM enrollments;


-- TASK 2: ALTER AND EXTEND THE SCHEMA

SELECT * FROM students WHERE enrollment_year=2022 ORDER BY last_name ASC;
SELECT * FROM courses WHERE credits>3 ORDER BY credits DESC;
SELECT * FROM PROFESSORS WHERE salary BETWEEN 80000 AND 95000;
SELECT * FROM students WHERE email LIKE '%@college.edu';
SELECT enrollment_year, count(*) FROM students GROUP BY enrollment_year;


-- TASK 3: MULTI-TABLE JOINS

SELECT concat(s.first_name," ", s.last_name) as full_name, d.dept_name from students s join departments d on s.department_id=d.department_id;
SELECT e.enrollment_id, s.first_name as Student_Name, c.course_name, e.enrollment_date, e.grade from enrollments e JOIN students s ON e.student_id=s.student_id JOIN courses c ON e.course_id=c.course_id;
SELECT s.student_id, CONCAT(s.first_name, ' ', s.last_name) AS student_name FROM students s LEFT JOIN enrollments e ON s.student_id = e.student_id WHERE e.enrollment_id IS NULL;
SELECT c.course_id, c.course_name, COUNT(e.student_id) AS total_students FROM courses c LEFT JOIN enrollments e ON c.course_id = e.course_id GROUP BY c.course_id, c.course_name ORDER BY c.course_id;
SELECT d.dept_name, p.prof_name, p.salary FROM departments d LEFT JOIN professors p ON d.department_id = p.department_id ORDER BY d.dept_name, p.prof_name;


-- TASK 4: AGGREGATIONS AND GROUPING

SELECT c.course_name, COUNT(e.enrollment_id) AS enrollment_count FROM courses c LEFT JOIN enrollments e ON c.course_id = e.course_id GROUP BY c.course_id, c.course_name ORDER BY enrollment_count DESC;
SELECT d.dept_name, ROUND(AVG(p.salary), 2) AS avg_salary FROM departments d LEFT JOIN professors p ON d.department_id = p.department_id GROUP BY d.department_id, d.dept_name;
SELECT department_id, dept_name, budget FROM departments WHERE budget > 600000;
SELECT e.grade, COUNT(*) AS grade_count FROM enrollments e JOIN courses c ON e.course_id = c.course_id WHERE c.course_code = 'CS101' GROUP BY e.grade ORDER BY e.grade;
SELECT d.dept_name, COUNT(DISTINCT s.student_id) AS total_students FROM departments d JOIN students s ON d.department_id = s.department_id GROUP BY d.department_id, d.dept_name HAVING COUNT(DISTINCT s.student_id) > 2;