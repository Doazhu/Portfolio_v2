from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config import settings

if settings.DATABASE_URL.startswith("postgres"):
    DATABASE_URL = settings.DATABASE_URL.replace("postgres://", "postgresql+asyncpg://")
elif settings.DATABASE_URL.startswith("sqlite:///"):
    DATABASE_URL = settings.DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///")
else:
    DATABASE_URL = "sqlite+aiosqlite:///portfolio.db"

engine = create_async_engine(DATABASE_URL, echo=settings.DEBUG)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with async_session() as session:
        yield session

