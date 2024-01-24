from fastapi import APIRouter, Depends
from sqlmodel import Session

from api.database import get_session
from api.public.special_prayer.crud import (
    add_special_prayer,
    get_masjid_special_prayers,
    update_masjid_special_prayer,
)
from api.public.special_prayer.models import SpecialPrayer, SpecialPrayerCreate
from api.utils.logger import logger_config

from api.auth.authenticate import auth_access_wrapper
from api.auth.utils import check_user_masjid_update_privileges

router = APIRouter()

logger = logger_config(__name__)


@router.get("", response_model=SpecialPrayer)
def get_a_masjid_special_prayers(masjid_id: str, db: Session = Depends(get_session)):
    logger.info("%s.get_a_masjid_special_prayers: %s", __name__, db)
    return get_masjid_special_prayers(masjid_id=masjid_id, db=db)


@router.patch("/{special_prayer_id}", response_model=SpecialPrayer)
def update_a_masjid_special_prayer(
    special_prayer_id: str,
    special_prayer: SpecialPrayer,
    db: Session = Depends(get_session),
    user_request=Depends(auth_access_wrapper),
):
    logger.info("%s.update_a_masjid_special_prayer: %s", __name__, special_prayer)
    check_user_masjid_update_privileges(user_request, special_prayer.masjid_id)
    return update_masjid_special_prayer(special_prayer_id=special_prayer_id, special_prayer=special_prayer, db=db)


@router.post("", response_model=SpecialPrayerCreate)
def create_a_special_prayer(
    masjid_id: str,
    special_prayer: SpecialPrayerCreate,
    db: Session = Depends(get_session),
    user_request=Depends(auth_access_wrapper),
):
    logger.info("%s.create_a_special_prayer: %s", __name__, special_prayer)
    check_user_masjid_update_privileges(user_request, special_prayer.masjid_id)
    return add_special_prayer(masjid_id=masjid_id, special_prayer=special_prayer, db=db)
