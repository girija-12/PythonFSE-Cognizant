import mysql.connector
import time
from pathlib import Path
from dotenv import dotenv_values

conn = mysql.connector.connect( host="localhost", user="root", password=dotenv_values(r"Module3_DatabaseIntegration\Girija\.env").get("MYSQL_PASSWORD"), database="college_db")
cursor = conn.cursor()
start = time.time()
cursor.execute("""SELECT e.enrollment_id, s.first_name, s.last_name, c.course_name, e.grade FROM enrollments e JOIN students s ON e.student_id = s.student_id JOIN courses c ON e.course_id = c.course_id""")
rows = cursor.fetchall()
end = time.time()
print("1 query executed.")
print(f"Time: {end-start:.6f} seconds")

"""
Results:
Version 1 (N+1 Query Pattern):
13 queries executed in 0.018144 seconds.

Version 2 (Single JOIN Query):
1 query executed in 0.020236 seconds.

Comparison:
The N+1 approach performs multiple database round-trips, while the JOIN
approach retrieves all required data in a single round-trip.

Although execution times are similar for this small dataset, the JOIN
approach is more scalable and reduces database overhead.

In a real application with 10,000 enrollments, the N+1 version would
execute 1 initial query plus 10,000 additional queries (10,001 total),
whereas the JOIN version would still execute only 1 query.

Both approaches return identical data, but the JOIN query is much more efficient.
"""