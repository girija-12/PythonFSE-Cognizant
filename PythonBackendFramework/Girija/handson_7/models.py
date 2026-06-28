from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Department(Base):

    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    courses = relationship("Course", back_populates="department")
    students = relationship("Student", back_populates="department")


class Course(Base):

    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String, unique=True)
    credits = Column(Integer)

    department_id = Column(
        Integer,
        ForeignKey("departments.id"),
    )

    department = relationship("Department", back_populates="courses")

    enrollments = relationship(
        "Enrollment",
        back_populates="course",
    )


class Student(Base):

    __tablename__ = "students"

    id = Column(Integer, primary_key=True)

    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)

    department_id = Column(
        Integer,
        ForeignKey("departments.id"),
    )

    department = relationship(
        "Department",
        back_populates="students",
    )

    enrollments = relationship(
        "Enrollment",
        back_populates="student",
    )


class Enrollment(Base):

    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True)

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
    )

    course_id = Column(
        Integer,
        ForeignKey("courses.id"),
    )

    student = relationship(
        "Student",
        back_populates="enrollments",
    )

    course = relationship(
        "Course",
        back_populates="enrollments",
    )