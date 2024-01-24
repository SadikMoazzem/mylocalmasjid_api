from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from api.database import get_session
from api.public.prayer_times.crud import (
    batch_add_prayer_times,
    read_prayer_times,
    update_single_prayer_times,
)
from api.public.prayer_times.models import PrayerTimes, PrayerTimesCreate
from api.utils.logger import logger_config

router = APIRouter()

logger = logger_config(__name__)


@router.get("", response_model=list[PrayerTimes])
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
):
    logger.info("%s.update_prayer_times: triggered", __name__)
    update_single_prayer_times(id=prayer_times_id, prayer_times=PrayerTimes.model_validate(prayer_times), db=db)
    return prayer_times


@router.post("/batch", response_model=list[PrayerTimesCreate])
def batch_add_prayer_times(
    masjid_id: str,
    prayer_times: list[PrayerTimesCreate],
    db: Session = Depends(get_session),
):
    logger.info("%s.batch_add_prayer_times: triggered", __name__)
    batch_add_prayer_times(masjid_id=masjid_id, prayer_times=prayer_times, db=db)
    return prayer_times