from pydantic import BaseModel, EmailStr
class UserRegister(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class CourseCreate(BaseModel):
    name: str
    code: str
    credits: int