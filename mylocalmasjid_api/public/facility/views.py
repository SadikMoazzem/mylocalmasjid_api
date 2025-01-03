from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from mylocalmasjid_api.database import get_session
from mylocalmasjid_api.public.facility.crud import add_facility, get_masjid_facilities, update_masjid_facility
from mylocalmasjid_api.public.facility.models import Facility, FacilityCreate
from mylocalmasjid_api.utils.logger import logger_config

from mylocalmasjid_api.auth.authenticate import auth_access_wrapper
from mylocalmasjid_api.auth.utils import check_user_masjid_update_privileges

router = APIRouter()

logger = logger_config(__name__)


@router.get("", response_model=List[Facility])
def get_a_masjid_facilities(masjid_id: str, db: Session = Depends(get_session)):
    logger.info("%s.get_a_masjid_facilities: %s", __name__, db)
    return get_masjid_facilities(masjid_id=masjid_id, db=db)


@router.patch("/{facility_id}", response_model=Facility)
def update_a_masjid_facility(
    facility_id: str,
    facility: Facility,
    db: Session = Depends(get_session),
    current_user=Depends(auth_access_wrapper),
):
    logger.info("%s.update_a_masjid_facility: %s", __name__, facility)
    check_user_masjid_update_privileges(current_user, facility.masjid_id)
    return update_masjid_facility(id=facility_id, facility=facility, db=db, user=current_user)


@router.post("", response_model=FacilityCreate)
def create_a_facility(
    facility: FacilityCreate,
    db: Session = Depends(get_session),
    current_user=Depends(auth_access_wrapper),
):
    logger.info("%s.create_a_facility: %s", __name__, facility)
    check_user_masjid_update_privileges(current_user, facility.masjid_id)
    return add_facility(facility=facility, db=db, user=current_user)
