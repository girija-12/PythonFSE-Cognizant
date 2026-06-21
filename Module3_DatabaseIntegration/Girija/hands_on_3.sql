USE college_db;

-- TASK 1: SUB QUERIES
SELECT s.student_id, CONCAT(s.first_name, ' ', s.last_name) AS student_name, COUNT(e.course_id) AS courses_taken FROM students s JOIN enrollments e  ON s.student_id = e.student_id GROUP BY s.student_id, student_name  HAVING COUNT(e.course_id) > (SELECT AVG(course_count) FROM (SELECT COUNT(*) AS course_count FROM enrollments GROUP BY student_id) avg_table);
SELECT c.course_id, c.course_name FROM courses c WHERE EXISTS ( SELECT 1 FROM enrollments e WHERE e.course_id = c.course_id ) AND NOT EXISTS( SELECT 1 FROM enrollments e WHERE e.course_id = c.course_id AND (e.grade <> 'A' OR e.grade IS NULL));
SELECT p.professor_id, p.prof_name, p.salary, d.dept_name FROM professors p JOIN departments d ON p.department_id = d.department_id WHERE p.salary = (  SELECT MAX(p2.salary) FROM professors p2  WHERE p2.department_id = p.department_id );
SELECT * FROM( SELECT d.department_id, d.dept_name, ROUND(AVG(p.salary),2) AS avg_salary FROM departments d JOIN professors p ON d.department_id = p.department_id GROUP BY d.department_id, d.dept_name ) dept_avg WHERE avg_salary > 85000;

-- TASK 2: CREATING AND USING VIEWS
CREATE VIEW vw_student_enrollment_summary AS SELECT s.student_id, CONCAT(s.first_name,' ',s.last_name) AS student_name, d.dept_name, COUNT(e.course_id) AS total_courses, ROUND(AVG(CASE e.grade WHEN 'A' THEN 4 WHEN 'B' THEN 3 WHEN 'C' THEN 2 WHEN 'D' THEN 1 WHEN 'F' THEN 0 END), 2) AS gpa FROM students s JOIN departments d ON s.department_id = d.department_id LEFT JOIN enrollments e ON s.student_id = e.student_id GROUP BY s.student_id, student_name, d.dept_name;
CREATE VIEW vw_course_stats AS SELECT c.course_name, c.course_code, COUNT(e.enrollment_id) AS total_enrollments, ROUND(AVG(CASE e.grade WHEN 'A' THEN 4 WHEN 'B' THEN 3 WHEN 'C' THEN 2 WHEN 'D' THEN 1 WHEN 'F' THEN 0 END), 2) AS avg_gpa FROM courses c LEFT JOIN enrollments e ON c.course_id = e.course_id GROUP BY c.course_id, c.course_name, c.course_code;
SELECT * FROM vw_course_stats;
SELECT * FROM vw_student_enrollment_summary WHERE gpa > 3.0;
UPDATE vw_student_enrollment_summary SET gpa = 4.0 WHERE student_id = 1;
DROP VIEW IF EXISTS vw_course_stats;
DROP VIEW IF EXISTS vw_student_enrollment_summary;
CREATE VIEW vw_student_enrollment_summary AS SELECT student_id, first_name, last_name, department_id FROM students WHERE department_id = 1 WITH CHECK OPTION;
UPDATE vw_student_enrollment_summary SET department_id = 1 WHERE student_id = 1;

-- TASK 3: STORED PROCEDURES AND TRANSACTIONS
DELIMITER $$
CREATE PROCEDURE sp_enroll_student ( IN p_student_id INT, IN p_course_id INT, IN p_enrollment_date DATE )
BEGIN
    IF EXISTS
    ( SELECT 1 FROM enrollments WHERE student_id = p_student_id AND course_id = p_course_id )
    THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Student already enrolled in this course';
    ELSE
        INSERT INTO enrollments ( student_id, course_id, enrollment_date ) VALUES ( p_student_id, p_course_id, p_enrollment_date);
    END IF;
END$$
DELIMITER ;

CREATE TABLE department_transfer_log (log_id INT AUTO_INCREMENT PRIMARY KEY, student_id INT, old_department_id INT, new_department_id INT, transfer_date DATETIME DEFAULT CURRENT_TIMESTAMP );
DELIMITER $$
CREATE PROCEDURE sp_transfer_student (IN p_student_id INT, IN p_new_department INT)
BEGIN
    DECLARE v_old_department INT;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;
    START TRANSACTION;
    SELECT department_id INTO v_old_department FROM students WHERE student_id = p_student_id;
    UPDATE students SET department_id = p_new_department WHERE student_id = p_student_id;
    INSERT INTO department_transfer_log(student_id, old_department_id, new_department_id) VALUES( p_student_id, v_old_department, p_new_department );
    COMMIT;
END$$
DELIMITER ;

SELECT department_id FROM students WHERE student_id = 1;
CALL sp_transfer_student(1, 999);
SELECT department_id FROM students WHERE student_id = 1;

START TRANSACTION;
INSERT INTO enrollments (student_id, course_id, enrollment_date) VALUES (4,2,CURDATE());
SAVEPOINT first_insert;
INSERT INTO enrollments(student_id, course_id, enrollment_date) VALUES (999,2,CURDATE());
ROLLBACK TO first_insert;
COMMIT;
SELECT * FROM enrollments WHERE student_id = 4 AND course_id = 2;