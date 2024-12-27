from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select

from mylocalmasjid_api.database import get_session
from mylocalmasjid_api.public.location.models import Location, LocationCreate
from mylocalmasjid_api.utils.helpers import check_masjid_exists
from mylocalmasjid_api.utils.logger import logger_config

logger = logger_config(__name__)


def create_location(masjid_location: LocationCreate, db: Session = Depends(get_session)):
    location_to_db = LocationCreate.model_validate(masjid_location)
    # Convert masjid_id to string for check_masjid_exists
    masjid_id = str(location_to_db.masjid_id) if location_to_db.masjid_id else None
    check_masjid_exists(masjid_id, db)
    
    # Convert LocationCreate to Location before adding to db
    location_data = location_to_db.model_dump()
    db_location = Location(**location_data)
    
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location


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
