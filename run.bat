@echo off
title Mathflix Full‑Stack
echo 🚀 Starte Mathflix Full‑Stack...

REM Backend starten
echo 🔧 Starte Backend (FastAPI)...
start cmd /k "cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000"

REM Frontend starten
echo 🎨 Starte Frontend...
start cmd /k "cd frontend && python -m http.server 8080"

echo.
echo ========================================
echo 🔥 Mathflix läuft jetzt!
echo Backend:   http://localhost:8000
echo Frontend:  http://localhost:8080
echo ========================================
echo.
pause
