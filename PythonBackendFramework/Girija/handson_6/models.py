from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey


class Base(DeclarativeBase):
    pass


class Department(Base):

    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)

    name = Column(String)

    courses = relationship(
        "Course",
        back_populates="department",
    )


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

    department = relationship(
        "Department",
        back_populates="courses",
    )