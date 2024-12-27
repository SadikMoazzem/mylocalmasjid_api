from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List, Optional

from mylocalmasjid_api.database import get_session
from mylocalmasjid_api.public.logs.models import Log, LogCreate


def create_log(log: LogCreate, db: Session = Depends(get_session)) -> Log:
    log_entry = Log.model_validate(log)
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    return log_entry


def get_logs(
    masjid_id: Optional[str] = None,
    user_id: Optional[str] = None,
    entity_type: Optional[str] = None,
    entity_id: Optional[str] = None,
    db: Session = Depends(get_session)
) -> List[Log]:
    query = select(Log)
    
    if masjid_id:
        query = query.where(Log.masjid_id == masjid_id)
    if user_id:
        query = query.where(Log.user_id == user_id)
    if entity_type:
        query = query.where(Log.entity_type == entity_type)
    if entity_id:
        query = query.where(Log.entity_id == entity_id)
    
    # Order by most recent first
    query = query.order_by(Log.action_time.desc())
    
    logs = db.exec(query).all()
    return logs 