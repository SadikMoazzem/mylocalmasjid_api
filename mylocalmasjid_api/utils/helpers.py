from fastapi import HTTPException, status
from sqlmodel import Session, select

from mylocalmasjid_api.public.masjid.models import Masjid
from mylocalmasjid_api.public.config.models import Config

def check_masjid_exists(masjid_id: str, db: Session):
    masjid_exists = db.exec(select(Masjid).where(Masjid.id == masjid_id)).first()
    if not masjid_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Masjid not found with id: {masjid_id}",
        )
    if not masjid_exists.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Masjid is not active",
        )
    return masjid_exists

def get_hijri_adjustment(db: Session):
    adjustment_option = db.exec(select(Config).where(Config.config_option == "hijri_adjustment")).first()
    if not adjustment_option:
        return 0
    
    return int(adjustment_option.value)
