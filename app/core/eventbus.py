# app/core/eventbus.py
import asyncio
import traceback
from typing import Callable, Dict, List, Any, Coroutine


class EventBus:
    """
    Enterprise Event-Bus:
    - asynchron
    - mehrere Subscriber pro Event
    - Fire & Forget Queue
    - Middleware-Unterstützung
    - Fehlerisolierung
    """

    _subscribers: Dict[str, List[Callable]] = {}
    _middlewares: List[Callable[[str, Any], Coroutine]] = []
    _queue: asyncio.Queue = asyncio.Queue()
    _worker_started = False

    # -------------------------------
    # Events abonnieren
    # -------------------------------
    @classmethod
    def subscribe(cls, event_name: str, callback: Callable):
        cls._subscribers.setdefault(event_name, []).append(callback)

    # -------------------------------
    # Middleware registrieren
    # -------------------------------
    @classmethod
    def add_middleware(cls, middleware: Callable[[str, Any], Coroutine]):
        cls._middlewares.append(middleware)

    # -------------------------------
    # Event auslösen
    # -------------------------------
    @classmethod
    async def emit(cls, event_name: str, payload: Any):
        await cls._queue.put((event_name, payload))

        # Worker starten, falls nicht aktiv
        if not cls._worker_started:
            asyncio.create_task(cls._worker())
            cls._worker_started = True

    # -------------------------------
    # Event‑Verarbeitung (Worker)
    # -------------------------------
    @classmethod
    async def _worker(cls):
        while True:
            event_name, payload = await cls._queue.get()

            # Middleware‑Chain
            for m in cls._middlewares:
                try:
                    await m(event_name, payload)
                except Exception:
                    traceback.print_exc()

            # Subscriber ausführen
            if event_name in cls._subscribers:
                for subscriber in cls._subscribers[event_name]:
                    try:
                        result = subscriber(payload)
                        if asyncio.iscoroutine(result):
                            await result
                    except Exception:
                        traceback.print_exc()

            cls._queue.task_done()