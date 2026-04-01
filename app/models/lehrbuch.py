from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class LehrbuchSeite(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    band: str
    kapitel: str
    seite: int
    titel: str
    text: str

    tags: Optional[str] = None
    analyse_json: Optional[str] = None

    erstellt_am: datetime = Field(default_factory=datetime.utcnow)
    aktualisiert_am: datetime = Field(default_factory=datetime.utcnow)