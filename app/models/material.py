from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Material(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    titel: str
    text: str

    # Analyse‑Ergebnisse
    tags: Optional[str] = None
    analyse_json: Optional[str] = None

    erstellt_am: datetime = Field(default_factory=datetime.utcnow)