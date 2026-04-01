# app/pipelines/material_pipeline.py
import json
from sqlmodel import select
from core.eventbus import EventBus
from agents.material_analyse_agent import MaterialAnalyseAgent
from db import async_session
from models.material import Material
from models.kompetenz import Kompetenz
from services.material_service import MaterialService


async def analyse_material_event(material_id: int):
    async with async_session() as session:

        # 1) Material laden
        material = await session.get(Material, material_id)
        if not material:
            print("❌ Material nicht gefunden:", material_id)
            return

        # 2) Tags extrahieren
        tags = MaterialAnalyseAgent.extract_tags(material.text)

        # 3) Kompetenzen laden
        result = await session.exec(select(Kompetenz))
        kompetenzen = result.all()

        # 4) Ranking berechnen
        ranking = []
        for k in kompetenzen:
            score = MaterialAnalyseAgent.score_kompetenz_fit(material.text, k)
            if score > 0:
                ranking.append({"kompetenz_id": k.id, "score": score})

        ranking = sorted(ranking, key=lambda x: x["score"], reverse=True)

        # 5) Summary erzeugen
        summary = MaterialAnalyseAgent.generate_summary(material.text)

        # 6) JSON speichern
        analyse_json = json.dumps({
            "tags": tags,
            "summary": summary,
            "ranking": ranking[:5]  # Top 5
        }, ensure_ascii=False)

        material.tags = ",".join(tags)
        material.analyse_json = analyse_json

        await MaterialService.update(
            session,
            material,
            {"tags": material.tags, "analyse_json": analyse_json}
        )

        print("🔎 Materialanalyse abgeschlossen:", material_id)


# Event Registrierung
EventBus.subscribe("material_uploaded", analyse_material_event)