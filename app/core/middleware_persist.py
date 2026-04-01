# app/core/middleware_persist.py

import json
from db import async_session
from models.eventlog import EventLog

async def persist_event(event_name: str, payload):
    """
    Persistiert jedes Event im EventLog.
    Wird vom EventBus vor dem Subscriber ausgeführt.
    """
    # JSON serialisieren (falls payload kein reines Dict ist)
    try:
        payload_json = json.dumps(payload, ensure_ascii=False, default=str)
    except Exception as e:
        payload_json = json.dumps({"error": str(e)}, ensure_ascii=False)

    async with async_session() as session:
        log = EventLog(
            event_name=event_name,
            payload_json=payload_json,
        )
        session.add(log)
        await session.commit()