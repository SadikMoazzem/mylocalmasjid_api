from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select

from api.database import get_session
from api.public.facility.models import Facility, FacilityCreate
from api.utils.helpers import check_masjid_exists


def add_facility(facility: FacilityCreate, db: Session = Depends(get_session)):
    facility_to_add = FacilityCreate.model_validate(facility)

    db.add(facility_to_add)
    db.commit()
    db.refresh(facility_to_add)
    return facility_to_add


def get_masjid_facilities(masjid_id: str, db: Session = Depends(get_session)):
    check_masjid_exists(masjid_id, db)
    masjid_facilities = db.exec(select(Facility).where(Facility.masjid_id == masjid_id)).all()
    if not masjid_facilities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Masjid not found with id: {masjid_id}",
        )
    return masjid_facilities


def update_masjid_facility(id: str, facility: Facility, db: Session = Depends(get_session)):
    facility_to_update = db.exec(select(Facility).where(Facility.id == id)).first()
    if not facility_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Facility not found with id: {id}",
        )

    facility_data = facility.model_dump(exclude_unset=True)
    for key, value in facility_data.items():
        setattr(facility_to_update, key, value)

    db.add(facility_to_update)
    db.commit()
    db.refresh(facility_to_update)
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
