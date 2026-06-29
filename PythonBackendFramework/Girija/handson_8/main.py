from fastapi import (FastAPI, Depends, HTTPException, Response, status, Request,)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy import or_

from database import engine
from database import get_db

from models import Base
from models import Course

from schemas import CourseCreate
from schemas import CourseUpdate
from schemas import CourseResponse

app = FastAPI(
    title="REST API Best Practices",
    version="1.0",
)


@app.on_event("startup")
async def startup():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Task 1: Audit and Fix Resource Naming and HTTP Methods

@app.post(
    "/api/v1/courses/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_course(
    course: CourseCreate,
    response: Response,
    db: AsyncSession = Depends(get_db),
):

    obj = Course(**course.model_dump())

    db.add(obj)

    await db.commit()

    await db.refresh(obj)

    response.headers["Location"] = (
        f"/api/v1/courses/{obj.id}/"
    )

    return obj


@app.get(
    "/api/v1/courses/{id}",
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

    if course is None:

        raise HTTPException(
            status_code=404,
            detail={
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Course with id {id} does not exist",
                    "field": None,
                }
            },
        )

    return course


@app.put(
    "/api/v1/courses/{id}",
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

    if obj is None:

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


@app.patch(
    "/api/v1/courses/{id}",
    response_model=CourseResponse,
)
async def patch_course(
    id: int,
    course: CourseUpdate,
    db: AsyncSession = Depends(get_db),
):

    result = await db.execute(
        select(Course).where(Course.id == id)
    )

    obj = result.scalar_one_or_none()

    if obj is None:

        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    for key, value in course.model_dump(
        exclude_unset=True
    ).items():

        setattr(obj, key, value)

    await db.commit()

    await db.refresh(obj)

    return obj


@app.delete(
    "/api/v1/courses/{id}",
    status_code=204,
)
async def delete_course(
    id: int,
    db: AsyncSession = Depends(get_db),
):

    result = await db.execute(
        select(Course).where(Course.id == id)
    )

    obj = result.scalar_one_or_none()

    if obj is None:

        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    await db.delete(obj)

    await db.commit()

    return Response(status_code=204)


# Task 2: Versioning, Pagination and Standardised Error Responses

@app.get("/api/v1/courses/")
async def get_courses(
    request: Request,
    page: int = 1,
    page_size: int = 2,
    search: str | None = None,
    db: AsyncSession = Depends(get_db),
):

    query = select(Course)

    if search:

        query = query.where(
            or_(
                Course.name.ilike(f"%{search}%"),
                Course.code.ilike(f"%{search}%"),
            )
        )

    total = await db.scalar(
        select(func.count()).select_from(
            query.subquery()
        )
    )

    offset = (page - 1) * page_size

    result = await db.execute(
        query.offset(offset).limit(page_size)
    )

    courses = result.scalars().all()

    next_url = None

    previous_url = None

    if offset + page_size < total:

        next_url = (
            f"{request.url.path}"
            f"?page={page+1}&page_size={page_size}"
        )

    if page > 1:

        previous_url = (
            f"{request.url.path}"
            f"?page={page-1}&page_size={page_size}"
        )

    return {
        "count": total,
        "next": next_url,
        "previous": previous_url,
        "results": [
            CourseResponse.model_validate(i)
            for i in courses
        ],
    }