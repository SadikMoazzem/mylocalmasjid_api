from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select

from api.database import get_session
from api.public.location.models import Location, LocationCreate
from api.utils.helpers import check_masjid_exists
from api.utils.logger import logger_config

logger = logger_config(__name__)


def create_location(masjid_location: LocationCreate, db: Session = Depends(get_session)):
    location_to_db = LocationCreate.model_validate(masjid_location)
    check_masjid_exists(location_to_db.masjid_id, db)
    db.add(location_to_db)
    db.commit()
    db.refresh(location_to_db)
    return location_to_db


# Find nearest locations to lat lon
def nearest_location(lat: float, lon: float, db: Session = Depends(get_session)):
    pass
    # return masjids


def get_masjid_location(masjid_id: str, db: Session = Depends(get_session)):
    masjid_location = db.exec(select(Location).where(Location.masjid_id == masjid_id)).first()
    if not masjid_location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Masjid not found with id: {masjid_id}",
        )
    return masjid_location


def update_masjid_location(id:str, location: Location, db: Session = Depends(get_session)):
    location_to_update = db.exec(select(Location).where(Location.id == id)).first()
    if not location_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location not found with id: {id}",
        )

    location_data = location.model_dump(exclude_unset=True)
    for key, value in location_data.items():
        setattr(location_to_update, key, value)

    db.add(location_to_update)
    db.commit()
    db.refresh(location_to_update)
    return location_to_update
