from fastapi import APIRouter, Depends
from sqlmodel import Session

from api.database import get_session
from api.public.location.crud import create_location, get_masjid_location, update_masjid_location
from api.public.location.models import Location, LocationCreate
from api.utils.logger import logger_config

router = APIRouter()

logger = logger_config(__name__)


@router.get("", response_model=Location)
def get_a_masjid_location(masjid_id: str, db: Session = Depends(get_session)):
    logger.info("%s.get_a_masjid_location: %s", __name__, db)
    return get_masjid_location(masjid_id=masjid_id, db=db)


@router.patch("/{location_id}", response_model=Location)
def update_a_masjid_location(location_id: str, location: Location, db: Session = Depends(get_session)):
    logger.info("%s.update_a_masjid_location: %s", __name__, location)
    return update_masjid_location(id=location_id, location=location, db=db)


@router.post("", response_model=LocationCreate)
def create_a_location(location: LocationCreate, db: Session = Depends(get_session)):
    logger.info("%s.create_a_location: %s", __name__, location)
    return create_location(location=location, db=db)
