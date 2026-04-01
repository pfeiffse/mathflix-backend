# app/agents/baustein_generator_agent.py

class BausteinGeneratorAgent:

    @staticmethod
    def generiere(kompetenz_titel: str):
        return {
            "einstieg": f"Einführung ins Thema: {kompetenz_titel}",
            "erarbeitung": "Partnerarbeit + Beispielaufgaben.",
            "sicherung": "Tafelbild & Zusammenfassung.",
            "reflexion": "Kurze Rückmeldung (Daumenfeedback)."
        }