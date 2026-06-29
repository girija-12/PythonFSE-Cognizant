from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Boolean


class Base(DeclarativeBase):
    pass


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    email = Column(String, unique=True)

    hashed_password = Column(String)

    is_active = Column(Boolean, default=True)


class Course(Base):

    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)

    name = Column(String)

    code = Column(String)

    credits = Column(Integer)