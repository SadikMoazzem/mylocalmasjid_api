import uuid
from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel


class AnnouncementBase(SQLModel):
    __tablename__ = 'announcements'

    masjid_id: uuid.UUID = Field(foreign_key="masjids.id", nullable=True)

    date_issued: date

    date_expired: Optional[date]

    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "masjid_id": "East London Mosque",
                "date_issued": "2021-01-01",
                "date_expired": "2021-01-01",
                "message": "Wudu area is located in the basement"
            }
        }


class Announcement(AnnouncementBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class AnnouncementCreate(AnnouncementBase):
    pass
