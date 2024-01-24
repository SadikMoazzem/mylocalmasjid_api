from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from api.database import get_session
from api.public.prayer_times.crud import (
    batch_add_prayer_times,
    read_prayer_times,
    update_single_prayer_times,
)
from api.public.prayer_times.models import PrayerTimes, PrayerTimesRead, PrayerTimesCreate
from api.utils.logger import logger_config

from api.auth.authenticate import auth_access_wrapper
from api.auth.utils import check_user_masjid_update_privileges

router = APIRouter()

logger = logger_config(__name__)


@router.get("", response_model=list[PrayerTimesRead])
def get_prayer_times(
    masjid_id: str = "",
    date: str = "",
    limit: int = Query(default=1, lte=1),
    db: Session = Depends(get_session),
):
    logger.info("%s.get_prayer_times: triggered", __name__)
    return read_prayer_times(masjid_id=masjid_id, selected_date=date, limit=limit, db=db)


@router.patch("/${prayer_times_id}", response_model=PrayerTimes)
def update_prayer_times(
    prayer_times_id: str,
    prayer_times: PrayerTimes,
    db: Session = Depends(get_session),
    user_request=Depends(auth_access_wrapper),
):
    logger.info("%s.update_prayer_times: triggered", __name__)
    check_user_masjid_update_privileges(user_request, prayer_times.masjid_id)
    update_single_prayer_times(id=prayer_times_id, prayer_times=PrayerTimes.model_validate(prayer_times), db=db)
    return prayer_times


@router.post("/batch", response_model=list[PrayerTimesCreate])
def batch_add_prayer_times(
    masjid_id: str,
    prayer_times: list[PrayerTimesCreate],
    db: Session = Depends(get_session),
    user_request=Depends(auth_access_wrapper),
):
    logger.info("%s.batch_add_prayer_times: triggered", __name__)
    check_user_masjid_update_privileges(user_request, prayer_times.masjid_id)
    batch_add_prayer_times(masjid_id=masjid_id, prayer_times=prayer_times, db=db)
    return prayer_times
