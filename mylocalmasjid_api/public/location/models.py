import uuid

from sqlalchemy import PrimaryKeyConstraint
from sqlmodel import Field, SQLModel


class LocationBase(SQLModel):
    __tablename__ = 'locations'

    masjid_id: uuid.UUID = Field(foreign_key="masjids.id", nullable=True)

    geoHash: str

    city: str

    country: str

    full_address: str

    latitude: float

    longitude: float
    
    __table_args__ = (
        PrimaryKeyConstraint("id"),
        {},
    )
    class Config:
        json_schema_extra = {
            "example": {
                "masjid_id": "East London Mosque",
                "geoHash": "gcpv0y",
                "city": "London",
                "country": "United Kingdom",
                "full_address": "82-92 Whitechapel Rd, London E1 1JQ, United Kingdom",
                "latitude": 51.517,
                "longitude": -0.066
            }
        }


class Location(LocationBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class LocationCreate(LocationBase):
    pass
