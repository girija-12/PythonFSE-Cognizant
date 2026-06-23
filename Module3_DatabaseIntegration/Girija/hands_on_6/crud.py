# Task 2: CRUD Operations via ORM

from datetime import date
from sqlalchemy.orm import sessionmaker, joinedload
from models import engine, Department, Student, Course, Enrollment

Session = sessionmaker(bind=engine)
session = Session()

cs = Department(dept_name="Computer Science", head_of_dept="Dr. Kumar", budget=850000)
ec = Department(dept_name="Electronics", head_of_dept="Dr. Nair", budget=620000)
me = Department(dept_name="Mechanical", head_of_dept="Dr. Iyer", budget=540000)
session.add_all([cs, ec, me])
session.commit()

students = [Student(first_name="Arjun", last_name="Mehta", email="arjun@college.edu", department=cs, enrollment_year=2022),
    Student(first_name="Priya", last_name="Suresh", email="priya@college.edu", department=cs, enrollment_year=2022),
    Student(first_name="Rohan", last_name="Verma", email="rohan@college.edu", department=ec, enrollment_year=2021),
    Student(first_name="Sneha", last_name="Patel", email="sneha@college.edu", department=me, enrollment_year=2023),
    Student(first_name="Deepika", last_name="Rao", email="deepika@college.edu", department=cs, enrollment_year=2022)]
session.add_all(students)
session.commit()

course1 = Course(course_name="Data Structures", course_code="CS101", credits=4)
course2 = Course(course_name="Database Management Systems", course_code="CS102", credits=3)
course3 = Course(course_name="Object Oriented Programming", course_code="CS103", credits=4)
session.add_all([course1, course2, course3])
session.commit()

enrollments = [Enrollment(student=students[0], course=course1, enrollment_date=date.today(), grade="A"),
    Enrollment(student=students[0], course=course2, enrollment_date=date.today(), grade="B"),
    Enrollment(student=students[1], course=course1, enrollment_date=date.today(), grade="A"),
    Enrollment(student=students[4], course=course3, enrollment_date=date.today(), grade="A")]
session.add_all(enrollments)
session.commit()

cs_students = session.query(Student).join(Department).filter(Department.dept_name == "Computer Science").all()
for student in cs_students:
    print(student.first_name, student.last_name)

all_enrollments = session.query(Enrollment).all()
for enrollment in all_enrollments:
    print(enrollment.student.first_name, "->", enrollment.course.course_name)

student = session.query(Student).filter_by(email="arjun@college.edu").first()
if student:
    student.enrollment_year = 2023
    session.commit()

enrollment = session.query(Enrollment).first()
if enrollment:
    session.delete(enrollment)
    session.commit()
print("Remaining Enrollments:", session.query(Enrollment).count())

# Task 3: eager Loading to Fix N+1 Problem

optimized_enrollments = session.query(Enrollment).options(
    joinedload(Enrollment.student),
    joinedload(Enrollment.course)
).all()

for enrollment in optimized_enrollments:
    print(enrollment.student.first_name, "->", enrollment.course.course_name)

session.close()