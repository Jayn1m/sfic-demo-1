import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from backend.app.models import Base

# On Vercel serverless environment, the root is read-only, so use /tmp for SQLite
default_db = "sqlite+aiosqlite:////tmp/botad_grievances.db" if os.getenv("VERCEL") else "sqlite+aiosqlite:///./botad_grievances.db"
DATABASE_URL = os.getenv("DATABASE_URL", default_db)

engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=False
)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with async_session() as session:
        yield session

