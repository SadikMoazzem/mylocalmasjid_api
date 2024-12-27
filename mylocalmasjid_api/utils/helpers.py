from fastapi import HTTPException, status
from sqlmodel import Session, select
import uuid

from mylocalmasjid_api.public.masjid.models import Masjid
from mylocalmasjid_api.public.config.models import Config
from mylocalmasjid_api.public.logs.models import LogCreate, ActionType
from mylocalmasjid_api.public.logs.crud import create_log
from mylocalmasjid_api.auth.models import User

def check_masjid_exists(masjid_id: str, db: Session):
    try:
        # Convert string to UUID for comparison
        masjid_uuid = uuid.UUID(masjid_id) if isinstance(masjid_id, str) else masjid_id
        masjid_exists = db.exec(select(Masjid).where(Masjid.id == masjid_uuid)).first()
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
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid masjid ID format: {masjid_id}",
        )

def get_hijri_adjustment(db: Session):
    adjustment_option = db.exec(select(Config).where(Config.config_option == "hijri_adjustment")).first()
    if not adjustment_option:
        return 0
    
    return int(adjustment_option.value)

def create_activity_log(
    db: Session,
    user: User,
    action: ActionType,
    entity_type: str,
    entity_id: uuid.UUID,
    masjid_id: uuid.UUID = None,
    details: str = None
) -> None:
    """Helper function to create activity logs from anywhere in the application."""
    log_entry = LogCreate(
        user_id=user.id,
        masjid_id=masjid_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        details=details
    )
    create_log(log_entry, db)
