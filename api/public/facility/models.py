import uuid
from typing import Optional

from sqlmodel import Field, SQLModel


class FacilityBase(SQLModel):
    __tablename__ = 'facilities'

    masjid_id: uuid.UUID = Field(foreign_key="masjids.id", nullable=False)

    facility: str

    info: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "masjid_id": "East London Mosque",
                "facility": "Wudu",
                "info": "Wudu area is located in the basement"
            }
        }


class Facility(FacilityBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class FacilityCreate(FacilityBase):
    pass
