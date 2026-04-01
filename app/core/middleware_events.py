# app/core/middleware_events.py

import datetime

async def log_event(event_name: str, payload):
    """
    Einfache Logging-Middleware für den EventBus.
    Wird vor jedem Event ausgeführt.
    """
    print(f"[EVENT] {datetime.datetime.now()} – {event_name}: {payload}")