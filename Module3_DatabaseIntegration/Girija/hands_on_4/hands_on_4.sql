USE college_db;

-- TASK 1: BASELINE PERFORMANCE-NO INDEXES

EXPLAIN FORMAT=JSON SELECT s.student_id, CONCAT(s.first_name, ' ', s.last_name) AS student_name, c.course_name, e.grade FROM students s JOIN enrollments e ON s.student_id = e.student_id JOIN courses c ON e.course_id = c.course_id;
/*
{
  "query_block": {
    "select_id": 1,
    "cost_info": {
      "query_cost": "8.87"
    },
    "nested_loop": [
      {
        "table": {
          "table_name": "c",
          "access_type": "ALL",
          "possible_keys": [
            "PRIMARY"
          ],
          "rows_examined_per_scan": 5,
          "rows_produced_per_join": 5,
          "filtered": "100.00",
          "cost_info": {
            "read_cost": "0.25",
            "eval_cost": "0.50",
            "prefix_cost": "0.75",
            "data_read_per_join": "3K"
          },
          "used_columns": [
            "course_id",
            "course_name"
          ]
        }
      },
      {
        "table": {
          "table_name": "e",
          "access_type": "ref",
          "possible_keys": [
            "student_id",
            "course_id"
          ],
          "key": "course_id",
          "used_key_parts": [
            "course_id"
          ],
          "key_length": "5",
          "ref": [
            "college_db.c.course_id"
          ],
          "rows_examined_per_scan": 2,
          "rows_produced_per_join": 12,
          "filtered": "100.00",
          "cost_info": {
            "read_cost": "2.50",
            "eval_cost": "1.25",
            "prefix_cost": "4.50",
            "data_read_per_join": "400"
          },
          "used_columns": [
            "student_id",
            "course_id",
            "grade"
          ],
          "attached_condition": "(`college_db`.`e`.`student_id` is not null)"
        }
      },
      {
        "table": {
          "table_name": "s",
          "access_type": "eq_ref",
          "possible_keys": [
            "PRIMARY"
          ],
          "key": "PRIMARY",
          "used_key_parts": [
            "student_id"
          ],
          "key_length": "4",
          "ref": [
            "college_db.e.student_id"
          ],
          "rows_examined_per_scan": 1,
          "rows_produced_per_join": 12,
          "filtered": "100.00",
          "cost_info": {
            "read_cost": "3.12",
            "eval_cost": "1.25",
            "prefix_cost": "8.88",
            "data_read_per_join": "10K"
          },
          "used_columns": [
            "student_id",
            "first_name",
            "last_name"
          ]
        }
      }
    ]
  }
}

Observation:
The query plan shows a Full Table Scan (ALL) on the courses table. The estimated query cost is 8.87, and the courses table examines 5 rows during the scan.
*/

CREATE INDEX idx_students_enrollment_year ON students(enrollment_year);
CREATE UNIQUE INDEX idx_enrollment_unique ON enrollments(student_id, course_id); 
CREATE INDEX idx_course_code ON courses(course_code);

EXPLAIN FORMAT=JSON SELECT s.student_id, CONCAT(s.first_name, ' ', s.last_name) AS student_name, c.course_name, e.grade FROM students s JOIN enrollments e ON s.student_id = e.student_id JOIN courses c ON e.course_id = c.course_id;
/* The Full Table Scan (ALL) moved from the courses table to the enrollments table. Both courses and students are accessed using efficient eq_ref primary key lookups. The query cost increased slightly from 8.87 to 9.05, with no major performance improvement.*/

CREATE INDEX idx_enrollments_grade_student ON enrollments(grade, student_id);

-- TASK 3: IDENTIFY AND FIX THE N+1 PROBLEM
-- Refer the python file