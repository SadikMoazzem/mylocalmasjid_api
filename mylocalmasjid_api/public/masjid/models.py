import uuid
from typing import Optional

from sqlmodel import Field, SQLModel


class MasjidBase(SQLModel):
    __tablename__ = 'masjids'

    name: str
    # TODO - Add Enums
    type: str
    locale: Optional[str]
    madhab: Optional[str]
    website: Optional[str]
    has_times: bool
    active: bool = Field(default=True)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "East London Mosque",
                "type": "Masjid",
                "locale": "English",
                "madhab": "Hanafi",
                "website": "https://www.eastlondonmosque.com/",
            }
        }


class Masjid(MasjidBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class MasjidCreate(MasjidBase):
    pass


class MasjidRead(MasjidBase):
    id: uuid.UUID


class MasjidUpdate(MasjidBase):
    name: str
    type: str
    locale: str
    madhab: str
