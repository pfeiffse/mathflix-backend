# app/agents/material_analyse_agent.py
import re
from typing import List
from models.kompetenz import Kompetenz


class MaterialAnalyseAgent:
    """
    Regelbasierte Analyse + KI‑Hook
    Extrahiert Tags aus einem Text und bewertet Kompetenz-Fit.
    """

    @staticmethod
    def extract_tags(text: str) -> List[str]:
        t = text.lower()
        tags = []

        keywords = {
            "gleichung": "Gleichungen",
            "funktion": "Funktionen",
            "dreieck": "Geometrie",
            "fläche": "Geometrie",
            "prozent": "Prozentrechnung",
            "diagramm": "Daten/Statistik",
            "wahrscheinlichkeit": "Wahrscheinlichkeit"
        }

        for word, tag in keywords.items():
            if word in t:
                tags.append(tag)

        # generisches mathematisches Muster
        if re.search(r"[0-9]+x", t):
            tags.append("Algebra")

        if re.search(r"f\\(x\\)", t):
            tags.append("Funktionen")

        return list(set(tags))

    @staticmethod
    def score_kompetenz_fit(material_text: str, kompetenz: Kompetenz) -> float:
        """
        Bewertung: Text-Tag gegen Kompetenz-Tags
        """
        score = 0
        k_tags = (kompetenz.tags or "").lower().split(",")

        for tag in k_tags:
            tag = tag.strip()
            if not tag:
                continue
            if tag in material_text.lower():
                score += 1

        return score

    @staticmethod
    def generate_summary(text: str) -> str:
        """
        simple KI‑Platzhalter: Rückgabe der ersten 180 Zeichen
        """
        return text.strip()[:180]