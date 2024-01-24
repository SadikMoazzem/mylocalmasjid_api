import datetime
import uuid
from typing import Optional

from sqlmodel import Field, SQLModel


# TODO - Add Optionals to all fields
# TODO - OnDelete Cascade
class PrayerTimesBase(SQLModel):
    __tablename__ = 'prayer_times'
    
    masjid_id: uuid.UUID = Field(foreign_key="masjids.id", nullable=True)

    date: datetime.date

    active: bool = Field(default=True)

    fajr_start: datetime.time

    fajr_jammat: datetime.time

    sunrise: datetime.time

    dhur_start: datetime.time

    dhur_jammat: datetime.time

    asr_start: datetime.time

    asr_start_1: Optional[datetime.time]

    asr_jammat: datetime.time

    magrib_start: datetime.time

    magrib_jammat: datetime.time

    isha_start: datetime.time

    isha_jammat: datetime.time

    class Config:
        json_schema_extra = {
            "example": {
                "masjid_id": "East London Mosque",
                "date": "2021-08-01",
                "fajr_start": "04:00:00",
                "fajr_jammat": "04:30:00",
                "sunrise": "05:00:00",
                "dhur_start": "12:00:00",
                "dhur_jammat": "12:30:00",
                "asr_start": "15:00:00",
                "asr_start_1": "15:30:00",
                "asr_jammat": "16:00:00",
                "magrib_start": "18:00:00",
                "magrib_jammat": "18:30:00",
                "isha_start": "21:00:00",
                "isha_jammat": "21:30:00"
            }
        }


class PrayerTimes(PrayerTimesBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class PrayerTimesRead(PrayerTimesBase):
    id: uuid.UUID
    hijri_date: str

class PrayerTimesCreate(PrayerTimesBase):
    pass
