from fastapi import APIRouter, Depends
from sqlmodel import Session

from api.database import get_session
from api.public.announcement.crud import (
    add_announcement,
    get_masjid_announcements,
    update_masjid_announcement,
)
from api.public.announcement.models import Announcement, AnnouncementCreate
from api.utils.logger import logger_config

router = APIRouter()

logger = logger_config(__name__)


@router.get("", response_model=Announcement)
def get_a_masjid_announcements(masjid_id: str, db: Session = Depends(get_session)):
    logger.info("%s.get_a_masjid_announcements: %s", __name__, db)
    return get_masjid_announcements(masjid_id=masjid_id, db=db)


@router.patch("/{announcement_id}", response_model=Announcement)
def update_a_masjid_announcement(announcement_id: str, announcement: Announcement, db: Session = Depends(get_session)):
    logger.info("%s.update_a_masjid_announcement: %s", __name__, announcement)
    return update_masjid_announcement(id=announcement_id, announcement=announcement, db=db)


@router.post("", response_model=AnnouncementCreate)
def create_a_announcement(announcement: AnnouncementCreate, db: Session = Depends(get_session)):
    logger.info("%s.create_a_announcement: %s", __name__, announcement)
    return add_announcement(announcement=announcement, db=db)
