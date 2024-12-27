import uuid
import enum
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class ActionType(str, enum.Enum):
    create = "create"
    update = "update"
    delete = "delete"


class LogBase(SQLModel):
    __tablename__ = 'logs'

    masjid_id: uuid.UUID = Field(foreign_key="masjids.id", nullable=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", nullable=False)
    action_time: datetime = Field(default_factory=datetime.utcnow)
    action: ActionType
    entity_type: str  # e.g. "prayer_times", "facility", etc.
    entity_id: uuid.UUID
    details: Optional[str]  # Additional context about the action

    class Config:
        json_schema_extra = {
            "example": {
                "masjid_id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "123e4567-e89b-12d3-a456-426614174001",
                "action_time": "2024-01-25T12:00:00Z",
                "action": "create",
                "entity_type": "prayer_times",
                "entity_id": "123e4567-e89b-12d3-a456-426614174002",
                "details": "Created new prayer times for date 2024-01-25"
            }
        }


class Log(LogBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class LogCreate(LogBase):
    pass 