from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Kompetenz(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    kompetenz_code: str = Field(index=True)
    titel: str
    jahrgang: str = Field(index=True)
    bereich: str
    beschreibung: Optional[str] = None

    # Mehrere Tags, z.B. "Terme,Gleichungen,Lineare Funktionen"
    tags: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)