# app/agents/stundenplan_agent.py
import json
from typing import List
from models.baustein import Baustein
from models.lehrbuch import LehrbuchSeite


class StundenplanAgent:

    @staticmethod
    def generiere_plan(
        kompetenz_titel: str,
        bausteine: List[Baustein],
        lehrbuchseiten: List[LehrbuchSeite],
        dauer_min: int = 45
    ):
        if not bausteine:
            return {"error": "Keine Bausteine vorhanden"}

        # Erster Baustein ist der Kern
        kern = bausteine[0]

        einstieg = kern.einstieg or f"Einführung in {kompetenz_titel}"
        erarbeitung = kern.erarbeitung or "Erarbeitung durch Aufgaben."
        sicherung = kern.sicherung or "Sicherung der Erkenntnisse."
        reflexion = kern.reflexion or "Reflexion der Stunde."

        lehrbuch_refs = [
            {"seite": l.seite, "titel": l.titel}
            for l in lehrbuchseiten[:2]
        ]

        plan = {
            "kompetenz": kompetenz_titel,
            "dauer_min": dauer_min,
            "ablauf": [
                {"phase": "Einstieg", "beschreibung": einstieg, "dauer": 5},
                {"phase": "Erarbeitung", "beschreibung": erarbeitung, "dauer": dauer_min - 15},
                {"phase": "Sicherung", "beschreibung": sicherung, "dauer": 7},
                {"phase": "Reflexion", "beschreibung": reflexion, "dauer": 3},
            ],
            "lehrbuch": lehrbuch_refs,
        }

        return plan