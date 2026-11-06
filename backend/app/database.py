import os
import sys
import shutil
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
    # AWS Lambda / Vercel Serverless filesystem is read-only except /tmp
    tmp_db_path = "/tmp/botad_grievances.db"
    if not os.path.exists(tmp_db_path):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        candidates = [
            "./botad_grievances.db",
            "/var/task/botad_grievances.db",
            os.path.join(current_dir, "..", "..", "botad_grievances.db")
        ]
        for candidate in candidates:
            if os.path.exists(candidate):
                try:
                    shutil.copyfile(candidate, tmp_db_path)
                    os.chmod(tmp_db_path, 0o666)
                    print(f"[INIT] Copied bundled seed DB to {tmp_db_path}")
                    break
                except Exception as e:
                    print(f"Notice copying seed db: {e}")
    default_db = f"sqlite+aiosqlite:///{tmp_db_path}"
else:
    default_db = "sqlite+aiosqlite:///./botad_grievances.db"

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


