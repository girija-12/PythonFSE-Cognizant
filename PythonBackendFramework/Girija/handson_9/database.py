from sqlalchemy.ext.asyncio import (create_async_engine, async_sessionmaker, AsyncSession)

DATABASE_URL = "sqlite+aiosqlite:///./auth.db"

engine = create_async_engine(DATABASE_URL)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session