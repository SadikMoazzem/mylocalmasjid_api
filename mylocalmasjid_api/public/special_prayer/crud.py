from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select

from mylocalmasjid_api.database import get_session
from mylocalmasjid_api.public.special_prayer.models import SpecialPrayer, SpecialPrayerCreate
from mylocalmasjid_api.utils.helpers import check_masjid_exists


def add_special_prayer(masjid_id: str, special_prayer: SpecialPrayerCreate, db: Session = Depends(get_session)):
    special_prayer_to_add = SpecialPrayerCreate.model_validate(special_prayer)
    if special_prayer_to_add.masjid_id != masjid_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Masjid id in url does not match masjid id in body",
        )
    check_masjid_exists(masjid_id, db)
    db.add(special_prayer_to_add)
    db.commit()
    db.refresh(special_prayer_to_add)
    return special_prayer_to_add

# Add in filter for date_issued and date_expired
def get_masjid_special_prayers(masjid_id: str, db: Session = Depends(get_session)):
    check_masjid_exists(masjid_id, db)
    masjid_special_prayers = db.exec(select(SpecialPrayer).where(SpecialPrayer.masjid_id == masjid_id)).all()
    if not masjid_special_prayers:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Masjid not found with id: {masjid_id}",
        )
    return masjid_special_prayers


def update_masjid_special_prayer(id: str, special_prayer: SpecialPrayer, db: Session = Depends(get_session)):
    check_masjid_exists(special_prayer.masjid_id, db)
    if special_prayer.id != id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"id in url does not match id in body",
        )

    special_prayer_to_update = db.exec(select(SpecialPrayer).where(SpecialPrayer.id == id)).first()
    if not special_prayer_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found with id: {id}",
        )

    special_prayer_data = SpecialPrayer.model_dump(exclude_unset=True)
    for key, value in special_prayer_data.items():
        setattr(special_prayer_to_update, key, value)

    db.add(special_prayer_to_update)
    db.commit()
    db.refresh(special_prayer_to_update)
    return special_prayer_to_update
