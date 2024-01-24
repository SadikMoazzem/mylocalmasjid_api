from fastapi import APIRouter, Depends
from sqlmodel import Session

from api.database import get_session
from api.public.facility.crud import add_facility, get_masjid_facilities, update_masjid_facility
from api.public.facility.models import Facility, FacilityCreate
from api.utils.logger import logger_config

router = APIRouter()

logger = logger_config(__name__)


@router.get("", response_model=Facility)
def get_a_masjid_facilities(masjid_id: str, db: Session = Depends(get_session)):
    logger.info("%s.get_a_masjid_facilities: %s", __name__, db)
    return get_masjid_facilities(masjid_id=masjid_id, db=db)


@router.patch("/{facility_id}", response_model=Facility)
def update_a_masjid_facility(facility_id: str, facility: Facility, db: Session = Depends(get_session)):
    logger.info("%s.update_a_masjid_facility: %s", __name__, facility)
    return update_masjid_facility(id=facility_id, facility=facility, db=db)


@router.post("", response_model=FacilityCreate)
def create_a_facility(facility: FacilityCreate, db: Session = Depends(get_session)):
    logger.info("%s.create_a_facility: %s", __name__, facility)
    return add_facility(facility=facility, db=db)
