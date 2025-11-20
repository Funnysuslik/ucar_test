from datetime import datetime
from enum import Enum

from sqlmodel import Field, SQLModel


class IncidentSource(str, Enum):
    operator = "operator"
    monitoring = "monitoring"
    partner = "partner"


class IncidentStatus(str, Enum):
    new = "new"
    investigating = "investigating"
    mitigated = "mitigated"
    resolved = "resolved"
    rejected = "rejected"


class IncidentBase(SQLModel):
    description: str
    source: IncidentSource
    status: IncidentStatus = Field(default=IncidentStatus.new)


class Incident(IncidentBase, table=True):
    __tablename__ = "incidents"

    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class IncidentCreate(IncidentBase):
    pass


class IncidentRead(Incident):
    pass


class IncidentUpdateStatus(SQLModel):
    status: IncidentStatus
