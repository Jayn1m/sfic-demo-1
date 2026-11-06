import os
import sys
from sqlalchemy import event
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from backend.app.models import Base

# Robust serverless / Vercel environment detection
is_serverless = (
    not sys.platform.startswith("win") and os.path.exists("/tmp")
) or bool(
    os.getenv("VERCEL") or 
    os.getenv("VERCEL_ENV") or 
    os.getenv("VERCEL_REGION") or 
    os.getenv("AWS_LAMBDA_FUNCTION_NAME") or 
    os.getenv("LAMBDA_TASK_ROOT")
)

if is_serverless:
    # On serverless environments, store database strictly in /tmp
    tmp_db_path = "/tmp/botad_grievances.db"
    
    # If a stale non-writable file exists in /tmp from prior runs, clean it up
    if os.path.exists(tmp_db_path):
        try:
            with open(tmp_db_path, "a") as f:
                pass
        except Exception:
            try:
                os.remove(tmp_db_path)
            except Exception:
                pass
                
    default_db = f"sqlite+aiosqlite:///{tmp_db_path}"
else:
    default_db = "sqlite+aiosqlite:///./botad_grievances.db"

DATABASE_URL = os.getenv("DATABASE_URL", default_db)

engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False, "timeout": 30} if "sqlite" in DATABASE_URL else {},
    echo=False
)

if "sqlite" in DATABASE_URL:
    @event.listens_for(engine.sync_engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=MEMORY")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.close()

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



