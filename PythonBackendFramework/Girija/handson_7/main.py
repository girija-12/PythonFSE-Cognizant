from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status,
    BackgroundTasks,
    Response,
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import engine, get_db
from models import Base
from models import Course
from models import Student
from models import Enrollment

from schemas import *
from typing import List

app = FastAPI(

    title="Course Management API",

    description="FastAPI CRUD API for Course Management",

    version="1.0",

    contact={
        "name": "Developer",
        "email": "developer@example.com",
    },
)


@app.on_event("startup")
async def startup():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Task 1: Complete CRUD with Proper HTTP Conventions

@app.post(
    "/api/courses/",
    tags=["Courses"],
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Course",
    response_description="Created Course",
)
async def create_course(
    course: CourseCreate,
    db: AsyncSession = Depends(get_db),
):

    obj = Course(**course.model_dump())

    db.add(obj)

    await db.commit()

    await db.refresh(obj)

    return obj


@app.get(
    "/api/courses/",
    tags=["Courses"],
    response_model=List[CourseResponse],
)
async def get_courses(
    db: AsyncSession = Depends(get_db),
):

    result = await db.execute(select(Course))

    return result.scalars().all()


@app.get(
    "/api/courses/{id}",
    tags=["Courses"],
    response_model=CourseResponse,
)
async def get_course(
    id: int,
    db: AsyncSession = Depends(get_db),
):

    result = await db.execute(
        select(Course).where(Course.id == id)
    )

    course = result.scalar_one_or_none()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    return course


@app.put(
    "/api/courses/{id}",
    tags=["Courses"],
    response_model=CourseResponse,
)
async def update_course(
    id: int,
    course: CourseCreate,
    db: AsyncSession = Depends(get_db),
):

    result = await db.execute(
        select(Course).where(Course.id == id)
    )

    obj = result.scalar_one_or_none()

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    obj.name = course.name
    obj.code = course.code
    obj.credits = course.credits
    obj.department_id = course.department_id

    await db.commit()
    await db.refresh(obj)

    return obj


@app.delete(
    "/api/courses/{id}",
    tags=["Courses"],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_course(
    id: int,
    db: AsyncSession = Depends(get_db),
):

    result = await db.execute(
        select(Course).where(Course.id == id)
    )

    obj = result.scalar_one_or_none()

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    await db.delete(obj)
    await db.commit()

    return Response(status_code=204)


@app.get(
    "/api/courses/{id}/students/",
    tags=["Courses"],
    response_model=List[StudentResponse],
)
async def get_course_students(
    id: int,
    db: AsyncSession = Depends(get_db),
):

    result = await db.execute(
        select(Student)
        .join(Enrollment)
        .where(Enrollment.course_id == id)
    )

    return result.scalars().all()


@app.post(
    "/api/students/",
    tags=["Students"],
    response_model=StudentResponse,
)
async def create_student(
    student: StudentCreate,
    db: AsyncSession = Depends(get_db),
):

    obj = Student(**student.model_dump())

    db.add(obj)

    await db.commit()

    await db.refresh(obj)

    return obj


@app.get(
    "/api/students/",
    tags=["Students"],
    response_model=List[StudentResponse],
)
async def get_students(
    db: AsyncSession = Depends(get_db),
):

    result = await db.execute(select(Student))

    return result.scalars().all()


# Task 2: Background Tasks and OpenAPI Customisation

def send_confirmation_email(email: str):

    print(f"Sending confirmation to {email}")


@app.post(
    "/api/enrollments/",
    tags=["Enrollments"],
    response_model=EnrollmentResponse,
    status_code=201,
)
async def create_enrollment(
    enrollment: EnrollmentCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):

    student = await db.get(
        Student,
        enrollment.student_id,
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    obj = Enrollment(**enrollment.model_dump())

    db.add(obj)

    await db.commit()

    await db.refresh(obj)

    background_tasks.add_task(
        send_confirmation_email,
        student.email,
    )

    return obj


@app.get(
    "/api/enrollments/",
    tags=["Enrollments"],
    response_model=List[EnrollmentResponse],
)
async def get_enrollments(
    db: AsyncSession = Depends(get_db),
):

    result = await db.execute(
        select(Enrollment)
    )

    return result.scalars().all()