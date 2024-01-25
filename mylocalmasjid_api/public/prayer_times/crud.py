from datetime import date

from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select

from mylocalmasjid_api.database import get_session
from mylocalmasjid_api.public.prayer_times.models import PrayerTimes, PrayerTimesRead, PrayerTimesCreate
from mylocalmasjid_api.utils.helpers import check_masjid_exists
from mylocalmasjid_api.utils.logger import logger_config

from mylocalmasjid_api.utils.hijri_date import HijriDate
from mylocalmasjid_api.utils.helpers import get_hijri_adjustment

logger = logger_config(__name__)

def read_prayer_times(masjid_id: str, limit = 1, selected_date: date = None, db: Session = Depends(get_session)):
    check_masjid_exists(masjid_id, db)

    prayer_times_query = select(PrayerTimes).where(PrayerTimes.masjid_id == masjid_id)
    if selected_date:
        prayer_times_query = prayer_times_query\
            .where(PrayerTimes.date >= selected_date)
    else:
        prayer_times_query = prayer_times_query\
            .where(PrayerTimes.date >= date.today())
    
    prayer_times = db.exec(prayer_times_query.order_by(PrayerTimes.date).limit(limit)).all()
    formatted_prayer_times = []
    adjustment = get_hijri_adjustment(db)

    for prayer_time in prayer_times:
        hijri = HijriDate.writeIslamicDate(date=prayer_time.date, adjustment=adjustment)

        prayer_time = PrayerTimesRead(
            **prayer_time.model_dump(),
            hijri_date=hijri['string'],
        )
        formatted_prayer_times.append(prayer_time.model_dump())
    
    return formatted_prayer_times


def update_single_prayer_times(id: str, prayer_times: PrayerTimes, db: Session = Depends(get_session)):
    prayer_times_row = db.exec(
        select(PrayerTimes).where(PrayerTimes.id == id)
    ).first()
    if not prayer_times_row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prayer Times not found with id: {id}",
        )
    
    logger.info("%s.update_single_prayer_times: %s", __name__, prayer_times)
    logger.info("%s.update_single_prayer_times [ROW]: %s", __name__, prayer_times_row)
    if prayer_times_row.date != prayer_times.date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Date in obj does not match date in body",
        )
    # Goes through new data and updates the row
    prayer_times_data = prayer_times.model_dump(exclude_unset=True)
    for key, value in prayer_times_data.items():
        setattr(prayer_times_row, key, value)

    db.add(prayer_times_row)
    db.commit()
    db.refresh(prayer_times_row)
    return prayer_times_row

def batch_add_prayer_times(masjid_id: str, prayer_times: list[PrayerTimesCreate], db: Session = Depends(get_session)):
    prayer_times_to_add = []

    for prayer_time in prayer_times:
        exists = db.exec(
            select(PrayerTimes).where(PrayerTimes.masjid_id == masjid_id).where(PrayerTimes.date == prayer_time.date)
        ).first()
        if exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Prayer Times Entry already exists for id: {masjid_id} and date: {date}",
            )
        PrayerTimesCreate.model_validate(prayer_time)
        prayer_time.masjid_id = masjid_id
        prayer_times_to_add.append(prayer_time)
    
    # Only adds if whole operation is successful
    db.add_all(prayer_times_to_add)
    db.commit()
    db.refresh(prayer_times_to_add)
    return prayer_times_to_add
