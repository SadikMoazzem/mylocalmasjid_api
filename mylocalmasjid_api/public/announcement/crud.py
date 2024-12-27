from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select

from mylocalmasjid_api.database import get_session
from mylocalmasjid_api.public.announcement.models import Announcement, AnnouncementCreate


def add_announcement(masjid_id: str, announcement: AnnouncementCreate, db: Session = Depends(get_session)):
    announcement_to_add = AnnouncementCreate.model_validate(announcement)
    # Convert both IDs to strings for comparison
    announcement_masjid_id = str(announcement_to_add.masjid_id) if announcement_to_add.masjid_id else None
    masjid_id = str(masjid_id) if masjid_id else None
    if announcement_masjid_id != masjid_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Masjid id in url does not match masjid id in body",
        )
    
    # Convert AnnouncementCreate to Announcement before adding to db
    announcement_data = announcement_to_add.model_dump()
    db_announcement = Announcement(**announcement_data)
    
    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)
    return db_announcement

# Add in filter for date_issued and date_expired
def get_masjid_announcements(masjid_id: str, db: Session = Depends(get_session)):
    masjid_announcements = db.exec(select(Announcement).where(Announcement.masjid_id == masjid_id)).all()
    if masjid_announcements is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No announcements found for masjid with id: {masjid_id}",
        )
    return masjid_announcements


def update_masjid_announcement(id:str, announcement: Announcement, db: Session = Depends(get_session)):
    # Convert both IDs to strings for comparison
    announcement_id = str(announcement.id) if announcement.id else None
    id = str(id) if id else None
    if announcement_id != id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"id in url does not match id in body",
        )

    announcement_to_update = db.exec(select(Announcement).where(Announcement.id == id)).first()
    if not announcement_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Announcement not found with id: {id}",
        )

    announcement_data = announcement.model_dump(exclude_unset=True)
    for key, value in announcement_data.items():
        setattr(announcement_to_update, key, value)

    db.add(announcement_to_update)
    db.commit()
    db.refresh(announcement_to_update)
    return announcement_to_update
