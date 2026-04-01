from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class EventLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    event_name: str
    payload_json: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)