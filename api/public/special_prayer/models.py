import enum
import uuid
from datetime import date, time
from typing import Optional

from sqlmodel import Field, SQLModel


class PrayerType(str, enum.Enum):
    jummuah = "jummuah"
    eid = "eid"

class SpecialPrayerBase(SQLModel):
    __tablename__ = 'special_prayers'

    masjid_id: uuid.UUID = Field(foreign_key="masjids.id", nullable=True)

    date: Optional[date]

    label: str

    # type: PrayerType = Field(sa_column=Column(Enum(PrayerType)))
    type: PrayerType = Field()

    info: Optional[str]

    imam: Optional[str]

    start_time: Optional[time]

    jammat_time: Optional[time]

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "masjid_id": "East London Mosque",
                "date": "2021-01-01",
                "label": "Jummuah",
                "type": "jummuah",
                "info": "Wudu area is located in the basement",
                "imam": "Muhammad",
                "start_time": "13:00",
                "jammat_time": "13:30"
            }
        }

class SpecialPrayer(SpecialPrayerBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class SpecialPrayerCreate(SpecialPrayerBase):
    pass
