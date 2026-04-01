#!/bin/bash
echo "🚀 Starte Mathflix Full‑Stack..."

# Backend starten
echo "🔧 Starte Backend (FastAPI)..."
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

BACKEND_PID=$!
cd ..

# Frontend starten (einfacher Python-Server)
echo "🎨 Starte Frontend..."
cd frontend
python3 -m http.server 8080 &

FRONTEND_PID=$!
cd ..

echo ""
echo "========================================"
echo "🔥 Mathflix läuft jetzt!"
echo "Backend:   http://localhost:8000"
echo "Frontend:  http://localhost:8080"
echo "========================================"
echo ""
echo "Zum Beenden: CTRL + C drücken."
echo ""

# Prozesse am Leben halten
wait $BACKEND_PID $FRONTEND_PID