from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select

from mylocalmasjid_api.database import get_session
from mylocalmasjid_api.public.facility.models import Facility, FacilityCreate
from mylocalmasjid_api.utils.helpers import check_masjid_exists, create_activity_log
from mylocalmasjid_api.public.logs.models import ActionType
from mylocalmasjid_api.auth.models import User


def add_facility(facility: FacilityCreate, db: Session = Depends(get_session), user: User = None):
    facility_to_add = Facility.model_validate(facility)

    db.add(facility_to_add)
    db.commit()
    db.refresh(facility_to_add)

    # Create log entry
    if user:
        create_activity_log(
            db=db,
            user=user,
            action=ActionType.create,
            entity_type="facility",
            entity_id=facility_to_add.id,
            masjid_id=facility_to_add.masjid_id,
            details=f"Created facility: {facility_to_add.facility}"
        )

    return facility_to_add


def get_masjid_facilities(masjid_id: str, db: Session = Depends(get_session)):
    check_masjid_exists(masjid_id, db)
    masjid_facilities = db.exec(select(Facility).where(Facility.masjid_id == masjid_id)).all()
    if masjid_facilities is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No facilities found for masjid with id: {masjid_id}",
        )
    return masjid_facilities


def update_masjid_facility(id: str, facility: Facility, db: Session = Depends(get_session), user: User = None):
    facility_to_update = db.exec(select(Facility).where(Facility.id == id)).first()
    if not facility_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Facility not found with id: {id}",
        )

    # Store old values for logging
    old_facility = facility_to_update.facility
    old_info = facility_to_update.info

    facility_data = facility.model_dump(exclude_unset=True)
    for key, value in facility_data.items():
        setattr(facility_to_update, key, value)

    db.add(facility_to_update)
    db.commit()
    db.refresh(facility_to_update)

    # Create log entry
    if user:
        details = f"Updated facility from '{old_facility}' to '{facility_to_update.facility}'"
        if old_info != facility_to_update.info:
            details += f", info updated"
        
        create_activity_log(
            db=db,
            user=user,
            action=ActionType.update,
            entity_type="facility",
            entity_id=facility_to_update.id,
            masjid_id=facility_to_update.masjid_id,
            details=details
        )

    return facility_to_update


# def delete_masjid(masjid_id: int, db: Session = Depends(get_session)):
#     masjid = db.get(Masjid, masjid_id)
#     if not masjid:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Team not found with id: {masjid_id}",
#         )

#     db.delete(masjid)
#     db.commit()
#     return {"ok": True}
