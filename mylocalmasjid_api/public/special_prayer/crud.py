from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select

from mylocalmasjid_api.database import get_session
from mylocalmasjid_api.public.special_prayer.models import SpecialPrayer, SpecialPrayerCreate
from mylocalmasjid_api.utils.helpers import check_masjid_exists


def add_special_prayer(masjid_id: str, special_prayer: SpecialPrayerCreate, db: Session = Depends(get_session)):
    # Convert masjid_id to UUID for comparison
    special_prayer_masjid_id = str(special_prayer.masjid_id) if special_prayer.masjid_id else None
    masjid_id = str(masjid_id) if masjid_id else None
    if special_prayer_masjid_id != masjid_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Masjid id in url does not match masjid id in body",
        )
    check_masjid_exists(masjid_id, db)
    
    # Convert SpecialPrayerCreate to SpecialPrayer
    special_prayer_data = special_prayer.model_dump()
    special_prayer_to_add = SpecialPrayer(**special_prayer_data)
    
    db.add(special_prayer_to_add)
    db.commit()
    db.refresh(special_prayer_to_add)
    return special_prayer_to_add


def get_masjid_special_prayers(masjid_id: str, db: Session = Depends(get_session)):
    check_masjid_exists(masjid_id, db)
    masjid_special_prayers = db.exec(select(SpecialPrayer).where(SpecialPrayer.masjid_id == masjid_id)).all()
    if masjid_special_prayers is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No special prayers found for masjid with id: {masjid_id}",
        )
    return masjid_special_prayers


def update_masjid_special_prayer(special_prayer_id: str, special_prayer: SpecialPrayer, db: Session = Depends(get_session)):
    check_masjid_exists(str(special_prayer.masjid_id), db)
    if str(special_prayer.id) != special_prayer_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"id in url does not match id in body",
        )

    special_prayer_to_update = db.exec(select(SpecialPrayer).where(SpecialPrayer.id == special_prayer_id)).first()
    if not special_prayer_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found with id: {special_prayer_id}",
        )

    special_prayer_data = special_prayer.model_dump(exclude_unset=True)
    for key, value in special_prayer_data.items():
        setattr(special_prayer_to_update, key, value)

    db.add(special_prayer_to_update)
    db.commit()
    db.refresh(special_prayer_to_update)
    return special_prayer_to_update
