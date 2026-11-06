import os
import sys
from sqlalchemy import event
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from backend.app.models import Base

# Robust serverless / Vercel environment detection
is_serverless = bool(
    os.getenv("VERCEL") or 
    os.getenv("VERCEL_ENV") or 
    os.getenv("VERCEL_REGION") or 
    os.getenv("AWS_LAMBDA_FUNCTION_NAME") or 
    os.getenv("LAMBDA_TASK_ROOT") or
    (not sys.platform.startswith("win") and os.path.exists("/tmp") and not os.path.exists("C:\\"))
)

env_db = os.getenv("DATABASE_URL", "")

if is_serverless:
    # On serverless (Vercel / AWS Lambda), the deployment directory (/var/task) is strictly read-only.
    # We MUST use the writable /tmp directory with 4 slashes for an absolute Unix path:
    # sqlite+aiosqlite:////tmp/botad_grievances.db
    if env_db and not ("sqlite" in env_db and ("./" in env_db or "botad_grievances" in env_db)):
        DATABASE_URL = env_db
    else:
        DATABASE_URL = "sqlite+aiosqlite:////tmp/botad_grievances.db"
else:
    DATABASE_URL = env_db or "sqlite+aiosqlite:///./botad_grievances.db"

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
        cursor.execute("PRAGMA busy_timeout=10000")
        cursor.close()

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

_db_initialized = False

async def init_db():
    global _db_initialized
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    _db_initialized = True

async def get_db():
    global _db_initialized
    if not _db_initialized:
        await init_db()
    async with async_session() as session:
        yield session
