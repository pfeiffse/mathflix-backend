# app/pipelines/lehrbuch_pipeline.py
import json
from sqlmodel import select
from core.eventbus import EventBus
from agents.lehrbuch_agent import LehrbuchAnalyseAgent
from db import async_session
from models.lehrbuch import LehrbuchSeite
from models.kompetenz import Kompetenz
from services.lehrbuch_service import LehrbuchService


async def analyse_lehrbuch_event(seite_id: int):
    async with async_session() as session:

        # 1) Lehrbuchseite laden
        seite = await session.get(LehrbuchSeite, seite_id)
        if not seite:
            print("❌ Lehrbuchseite nicht gefunden:", seite_id)
            return

        # 2) Tags extrahieren
        tags = LehrbuchAnalyseAgent.extract_tags(seite.text)

        # 3) Kompetenzen ranken
        result = await session.exec(select(Kompetenz))
        kompetenzen = result.all()

        ranking = []
        for k in kompetenzen:
            score = LehrbuchAnalyseAgent.kompetenz_score(seite.text, k)
            if score > 0:
                ranking.append({"kompetenz_id": k.id, "score": score})

        ranking = sorted(ranking, key=lambda x: x["score"], reverse=True)

        # 4) JSON speichern
        analyse_json = json.dumps({
            "tags": tags,
            "ranking": ranking[:5]
        }, ensure_ascii=False)

        await LehrbuchService.aktualisiere(session, seite, {
            "tags": ",".join(tags),
            "analyse_json": analyse_json
        })

        print("📘 Lehrbuch‑Analyse abgeschlossen:", seite_id)


# Event Registrierung
EventBus.subscribe("lehrbuchseite_uploaded", analyse_lehrbuch_event)