@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
echo ========================================================
echo  Starting Botad DDO Grievance AI Backend (FastAPI)
echo  Port: http://localhost:8000
echo  Swagger API Docs: http://localhost:8000/docs
echo ========================================================
call .\venv\Scripts\activate.bat
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
pause

