from sqlmodel import SQLModel, Field
from typing import Optional


class BausteinKompetenz(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    baustein_id: int = Field(foreign_key="baustein.id")
    kompetenz_id: int = Field(foreign_key="kompetenz.id")