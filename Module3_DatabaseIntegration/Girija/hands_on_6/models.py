## Task 1: SQLAlchemy — Define Models and Connect

from sqlalchemy import (create_engine, Column, Integer, String, Date, ForeignKey, DECIMAL)
from sqlalchemy.orm import (declarative_base, relationship)

engine = create_engine("mysql+pymysql://root:*MySQL01Girija@localhost/college_db_orm", echo=True)
Base = declarative_base()

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

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("All ORM tables created successfully.")