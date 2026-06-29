from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status,
)

from fastapi.middleware.cors import CORSMiddleware

from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from database import engine
from database import get_db

from models import Base
from models import User
from models import Course

from schemas import *

from security import *

app = FastAPI(
    title="Course Management API",
    version="1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


@app.on_event("startup")
async def startup():

    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all
        )


@app.post("/api/v1/auth/register")
async def register(
    user: UserRegister,
    db: AsyncSession = Depends(get_db),
):

    result = await db.execute(
        select(User).where(
            User.email == user.email
        )
    )

    existing = result.scalar_one_or_none()

    if existing:

        raise HTTPException(
            status_code=409,
            detail="Email already registered",
        )

    new_user = User(
        email=user.email,
        hashed_password=get_password_hash(
            user.password
        ),
    )

    db.add(new_user)

    await db.commit()

    return {
        "message": "User registered successfully"
    }


# Task 2: JWT Login, Protected Routes and CORS

@app.post("/api/v1/auth/login")
async def login(
    user: UserLogin,
    db: AsyncSession = Depends(get_db),
):

    result = await db.execute(
        select(User).where(
            User.email == user.email
        )
    )

    db_user = result.scalar_one_or_none()

    if (
        db_user is None
        or not verify_password(
            user.password,
            db_user.hashed_password,
        )
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    token = create_access_token(
        {"sub": db_user.email}
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }


async def get_current_user(
    token: str = Depends(
        oauth2_scheme
    ),
    db: AsyncSession = Depends(get_db),
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        email = payload.get("sub")

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )

    result = await db.execute(
        select(User).where(
            User.email == email
        )
    )

    user = result.scalar_one_or_none()

    if user is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid user",
        )

    return user


@app.get("/api/v1/courses/")
async def get_courses():

    return [
        {
            "id": 1,
            "name": "Python",
            "code": "CS101",
            "credits": 4,
        }
    ]


@app.post("/api/v1/courses/")
async def create_course(
    course: CourseCreate,
    current_user: User = Depends(
        get_current_user
    ),
):

    return {
        "message": "Course created",
        "course": course,
    }


@app.delete(
    "/api/v1/courses/{id}"
)
async def delete_course(
    id: int,
    current_user: User = Depends(
        get_current_user
    ),
):

    return {
        "message": "Course deleted"
    }