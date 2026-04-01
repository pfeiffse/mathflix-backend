from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Baustein(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Single- oder Multi-Kompetenz Zuordnung über Mapping
    kompetenz_id: Optional[int] = Field(default=None, foreign_key="kompetenz.id")

    titel: str
    beschreibung: Optional[str] = None

    # Unterrichtsphasen
    einstieg: Optional[str] = None
    erarbeitung: Optional[str] = None
    sicherung: Optional[str] = None
    reflexion: Optional[str] = None

    tags: Optional[str] = None

    erstellt_am: datetime = Field(default_factory=datetime.utcnow)
    aktualisiert_am: datetime = Field(default_factory=datetime.utcnow)