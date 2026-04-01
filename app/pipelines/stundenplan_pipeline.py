# app/pipelines/stundenplan_pipeline.py
from sqlmodel import select
from core.eventbus import EventBus
from db import async_session
from models.kompetenz import Kompetenz
from models.baustein import Baustein
from models.lehrbuch import LehrbuchSeite
from models.stundenplan import Stundenplan
from services.stundenplan_service import StundenplanService
from agents.stundenplan_agent import StundenplanAgent
import json


async def stundenplan_event(kompetenz_id: int):
    async with async_session() as session:

        # 1) Kompetenz laden
        k = await session.get(Kompetenz, kompetenz_id)
        if not k:
            print("❌ Kompetenz nicht gefunden:", kompetenz_id)
            return

        # 2) Bausteine laden
        b_stmt = select(Baustein).where(Baustein.kompetenz_id == kompetenz_id)
        bausteine = (await session.exec(b_stmt)).all()

        # 3) Lehrbuchseiten
        l_stmt = select(LehrbuchSeite)
        lehrbuch = (await session.exec(l_stmt)).all()

        # 4) Stundenplan generieren
        plan_data = StundenplanAgent.generiere_plan(
            k.titel, bausteine, lehrbuch
        )

        # 5) Speichern
        record = Stundenplan(
            titel=f"Stunde zu {k.titel}",
            kompetenz_id=kompetenz_id,
            plan_json=json.dumps(plan_data, ensure_ascii=False),
        )

        await StundenplanService.speichern(session, record)

        print("🕒 Stundenplan generiert:", record.id)


# Event Registrierung
EventBus.subscribe("generate_stundenplan", stundenplan_event)