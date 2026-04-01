from fastapi import FastAPI

from db import init_db
from routers import (
    kompetenzen_router,
    material_router,
    lehrbuch_router,
    bausteine_router,
    stundenplan_router,
)
from auth import router as auth_router

from core.eventbus import EventBus
from core.middleware_events import log_event
from core.middleware_persist import persist_event

app = FastAPI(title="Mathflix Enterprise Backend")

app.include_router(auth_router)
app.include_router(kompetenzen_router)
app.include_router(material_router)
app.include_router(lehrbuch_router)
app.include_router(bausteine_router)
app.include_router(stundenplan_router)

# -----------------------------
# Startup
# -----------------------------
@app.on_event("startup")
async def on_startup():
    await init_db()
    EventBus.add_middleware(log_event)
    EventBus.add_middleware(persist_event)
    print("🚀 Backend gestartet.")

@app.get("/")
async def root():
    return {"message": "Mathflix Backend läuft"}