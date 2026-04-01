# app/agents/lehrbuch_agent.py
import re
from models.kompetenz import Kompetenz


class LehrbuchAnalyseAgent:

    @staticmethod
    def extract_tags(text: str):
        t = text.lower()
        tags = []

        keywords = {
            "gleichung": "Gleichungen",
            "funktion": "Funktionen",
            "dreieck": "Geometrie",
            "fläche": "Geometrie",
            "prozent": "Prozentrechnung",
            "daten": "Daten/Statistik",
            "diagramm": "Daten/Statistik",
            "wahrscheinlichkeit": "Wahrscheinlichkeit"
        }

        for word, tag in keywords.items():
            if word in t:
                tags.append(tag)

        # lineare Funktionen Muster
        if re.search(r"y\\s*=\\s*m\\s*x", t):
            tags.append("Lineare Funktionen")

        return list(set(tags))

    @staticmethod
    def kompetenz_score(text: str, kompetenz: Kompetenz) -> float:
        score = 0
        for tag in (kompetenz.tags or "").lower().split(","):
            t = tag.strip()
            if t and t in text.lower():
                score += 1
        return score