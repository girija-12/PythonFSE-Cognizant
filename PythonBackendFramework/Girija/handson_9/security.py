from datetime import datetime, timedelta

from jose import jwt

from passlib.context import CryptContext

SECRET_KEY = "coursemanager-secret"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

# Task 1: Password Hashing and User Registration
# bcrypt is intentionally slow and includes a work factor, making brute-force attacks much harder than MD5 or SHA-256, which are designed for fast hashing and are unsuitable for password storage.


def get_password_hash(password: str):

    return pwd_context.hash(password)


def verify_password(
    plain_password,
    hashed_password,
):

    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update(
        {"exp": expire}
    )

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )