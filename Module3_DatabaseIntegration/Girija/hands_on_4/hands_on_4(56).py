import mysql.connector
import time
from dotenv import dotenv_values

conn = mysql.connector.connect( host="localhost", user="root", password=dotenv_values(r"Module3_DatabaseIntegration\Girija\.env").get("MYSQL_PASSWORD"), database="college_db")
cursor = conn.cursor()

cursor = conn.cursor()
query_count = 0 
start = time.time() 
cursor.execute(""" SELECT enrollment_id, student_id, course_id FROM enrollments """)
query_count += 1
enrollments = cursor.fetchall()
results = []
for enrollment in enrollments:
    student_id = enrollment[1]
    cursor.execute(""" SELECT first_name, last_name FROM students WHERE student_id = %s """, (student_id,))
    query_count += 1
    student = cursor.fetchone()
    results.append( ( enrollment[0], student[0], student[1] ) )
end = time.time()
print(f"{query_count} queries executed.")
print(f"Time: {end-start:.6f} seconds")