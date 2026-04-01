# app/models/lehrbuch_kompetenz.py

from sqlmodel import SQLModel, Field
from typing import Optional


class LehrbuchKompetenz(SQLModel, table=True):
    """
    Verknüpfungstabelle zwischen LehrbuchSeite und Kompetenz
    (Many-to-Many Mapping)
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    lehrbuchseite_id: int = Field(foreign_key="lehrbuchseite.id")
    kompetenz_id: int = Field(foreign_key="kompetenz.id")
