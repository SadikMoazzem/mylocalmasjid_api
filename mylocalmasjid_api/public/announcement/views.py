from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from mylocalmasjid_api.database import get_session
from mylocalmasjid_api.public.announcement.crud import (
    add_announcement,
    get_masjid_announcements,
    update_masjid_announcement,
)
from mylocalmasjid_api.public.announcement.models import Announcement, AnnouncementCreate
from mylocalmasjid_api.utils.logger import logger_config

from mylocalmasjid_api.auth.authenticate import auth_access_wrapper
from mylocalmasjid_api.auth.utils import check_user_masjid_update_privileges

router = APIRouter()

logger = logger_config(__name__)


@router.get("", response_model=List[Announcement])
def get_a_masjid_announcements(masjid_id: str, db: Session = Depends(get_session)):
    logger.info("%s.get_a_masjid_announcements: %s", __name__, db)
    return get_masjid_announcements(masjid_id=masjid_id, db=db)


@router.patch("/{announcement_id}", response_model=Announcement)
def update_a_masjid_announcement(
    masjid_id: str,
    announcement_id: str,
    announcement: Announcement,
    db: Session = Depends(get_session),
    user_request=Depends(auth_access_wrapper),
):
    logger.info("%s.update_a_masjid_announcement: %s", __name__, announcement)
    check_user_masjid_update_privileges(user_request, masjid_id)
    return update_masjid_announcement(id=announcement_id, announcement=announcement, db=db)


@router.post("", response_model=AnnouncementCreate)
def create_a_announcement(
    masjid_id: str,
    announcement: AnnouncementCreate,
    db: Session = Depends(get_session),
    user_request=Depends(auth_access_wrapper),
):
    logger.info("%s.create_a_announcement: %s", __name__, announcement)
    check_user_masjid_update_privileges(user_request, masjid_id)
    return add_announcement(masjid_id=masjid_id, announcement=announcement, db=db)
