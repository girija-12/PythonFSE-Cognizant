from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String


class Base(DeclarativeBase):
    pass


class Course(Base):

    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)

    name = Column(String)

    code = Column(String, unique=True)

    credits = Column(Integer)

    department_id = Column(Integer)