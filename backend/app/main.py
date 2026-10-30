import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from backend.app.database import init_db
from backend.app.services.sla_tracker import start_sla_scheduler
from backend.app.routers import complaints, admin

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables and launch background SLA scheduler
    print("[INIT] Creating SQLite tables...")
    await init_db()
    print("[INIT] Starting SLA deadline tracker background scheduler...")
    try:
        start_sla_scheduler()
    except Exception as e:
        print(f"Notice starting scheduler: {e}")
    yield
    # Shutdown

app = FastAPI(
    title="Botad DDO Citizen Grievance AI Redressal Platform",
    description="AI-based classification, routing, and deadline tracking of citizens' complaints using Gujarati voice and text.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(complaints.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {
        "status": "online",
        "system": "Botad District Grievance Redressal AI Platform (બોટાદ જિલ્લા ફરિયાદ નિવારણ પ્રણાલી)",
        "docs_url": "/docs"
    }

