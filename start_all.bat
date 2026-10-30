@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
echo =========================================================================
echo   District Development Office - Botad (Problem ID: PS000190)
echo   AI-based Grievance Redressal, Voice Intake ^& Deadline Tracking System
echo =========================================================================
echo.
echo [1/2] Launching Backend API Server (FastAPI on Port 8000)...
start "Botad AI Redressal Backend" cmd /c "run_backend.bat"

echo.
echo [2/2] Launching Frontend Citizen Portal (Vite React on Port 5173)...
start "Botad Citizen Portal Frontend" cmd /c "run_frontend.bat"

echo.
echo =========================================================================
echo   Both services are starting!
echo   - Citizen & DDO Portal: http://localhost:5173
echo   - Interactive API Docs: http://localhost:8000/docs
echo =========================================================================
echo.
pause

