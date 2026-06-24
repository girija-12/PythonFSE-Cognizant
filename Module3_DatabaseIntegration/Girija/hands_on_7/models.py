from sqlalchemy import create_engine, Column, Integer, String, Date, Time, Boolean, ForeignKey, DECIMAL
from sqlalchemy.orm import declarative_base, relationship

engine = create_engine( "mysql+pymysql://root:*MySQL01Girija@localhost/college_db_orm", echo=True)
Base = declarative_base()

# Task 1: Set Up Alembic and Create a Baseline Migration
class Department(Base):
    __tablename__ = "departments"
    department_id = Column(Integer, primary_key=True)
    dept_name = Column(String(100), nullable=False)
    head_of_dept = Column(String(100))
    budget = Column(DECIMAL(12, 2))
    students = relationship("Student", back_populates="department")
    professors = relationship("Professor", back_populates="department")

class Student(Base):
    __tablename__ = "students"
    student_id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    date_of_birth = Column(Date)
    department_id = Column(Integer, ForeignKey("departments.department_id"))
    enrollment_year = Column(Integer)
    is_active = Column(Boolean, default=True)
    department = relationship("Department", back_populates="students")
    enrollments = relationship("Enrollment", back_populates="student")

class Course(Base):
    __tablename__ = "courses"
    course_id = Column(Integer, primary_key=True)
    course_name = Column(String(150), nullable=False)
    course_code = Column(String(20), unique=True)
    credits = Column(Integer)
    department_id = Column(Integer, ForeignKey("departments.department_id"))
    enrollments = relationship("Enrollment", back_populates="course")
    schedules = relationship("CourseSchedule", back_populates="course")

class Enrollment(Base):
    __tablename__ = "enrollments"
    enrollment_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.student_id"))
    course_id = Column(Integer, ForeignKey("courses.course_id"))
    enrollment_date = Column(Date)
    grade = Column(String(2))
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

class Professor(Base):
    __tablename__ = "professors"
    professor_id = Column(Integer, primary_key=True)
    prof_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    department_id = Column(Integer, ForeignKey("departments.department_id"))
    salary = Column(DECIMAL(10, 2))
    department = relationship("Department", back_populates="professors")

# Task 2: Add and Apply Incremental Migrations
class CourseSchedule(Base):
    __tablename__ = "course_schedules"
    schedule_id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.course_id"))
    day_of_week = Column(String(20))
    start_time = Column(Time)
    end_time = Column(Time)
    course = relationship("Course", back_populates="schedules")

Base.metadata.create_all(engine)
print("Tables created successfully.")