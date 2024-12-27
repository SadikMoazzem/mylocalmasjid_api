import enum
import uuid
from datetime import date, time
from typing import Optional

from sqlmodel import Field, SQLModel


class PrayerType(str, enum.Enum):
    jummuah = "jummuah"
    eid = "eid"
    tahajud = "tahajud"
    taraweeh = "taraweeh"
    other = "other"

class SpecialPrayerBase(SQLModel):
    __tablename__ = 'special_prayers'

    masjid_id: uuid.UUID = Field(foreign_key="masjids.id", nullable=True)

    # Store dates in a single format
    date_start: Optional[date] = Field(nullable=True)
    date_end: Optional[date] = Field(nullable=True)
    
    # Whether the provided dates are Hijri
    is_hijri: bool = Field(default=False)

    label: str

    type: PrayerType = Field()

    info: Optional[str] = Field(nullable=True)

    imam: Optional[str] = Field(nullable=True)

    start_time: Optional[time] = Field(nullable=True)

    jammat_time: Optional[time] = Field(nullable=True)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "masjid_id": "East London Mosque",
                "date_start": "1445-05-17",
                "date_end": "1445-06-17",
                "is_hijri": True,
                "label": "Taraweeh",
                "type": "taraweeh",
                "info": "Ramadan night prayers",
                "imam": "Muhammad",
                "start_time": "22:00",
                "jammat_time": "22:15"
            }
        }

class SpecialPrayer(SpecialPrayerBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class SpecialPrayerCreate(SpecialPrayerBase):
    pass
