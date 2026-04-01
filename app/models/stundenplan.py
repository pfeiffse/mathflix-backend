from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Stundenplan(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    titel: str
    kompetenz_id: Optional[int] = Field(default=None, foreign_key="kompetenz.id")
    dauer_min: int = 45

    # JSON: Einstieg, Erarbeitung, Sicherung, Reflexion + Lehrbuchlinks
    plan_json: Optional[str] = None

    erstellt_am: datetime = Field(default_factory=datetime.utcnow)