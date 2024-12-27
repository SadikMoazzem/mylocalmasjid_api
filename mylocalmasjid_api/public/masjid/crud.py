from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select, or_
from typing import Optional

from mylocalmasjid_api.database import get_session
from mylocalmasjid_api.public.masjid.models import Masjid, MasjidCreate, MasjidUpdate, PaginatedMasjids


def create_masjid(masjid: MasjidCreate, db: Session = Depends(get_session)):
    masjid_to_db = Masjid.model_validate(masjid)
    db.add(masjid_to_db)
    db.commit()
    db.refresh(masjid_to_db)
    return masjid_to_db


def read_masjids(
    search: str = "",
    type_filter: Optional[str] = None,
    madhab_filter: Optional[str] = None,
    locale_filter: Optional[str] = None,
    page: int = 1,
    size: int = 20,
    db: Session = Depends(get_session),
    user = None,
) -> PaginatedMasjids:
    # Start with base query
    query = select(Masjid)
    
    # Filter based on user permissions
    if not user:
        # Return empty list for unauthenticated users
        return PaginatedMasjids(
            items=[],
            total=0,
            page=page,
            size=size,
            pages=0
        )
    elif user.role != "admin":
        # Masjid admin can only see their assigned masjid
        query = query.where(Masjid.id == user.related_masjid)
    
    # Apply search filter if provided
    if search:
        query = query.filter(
            or_(
                Masjid.name.ilike(f"%{search}%"),
                Masjid.type.ilike(f"%{search}%"),
                Masjid.locale.ilike(f"%{search}%"),
                Masjid.madhab.ilike(f"%{search}%")
            )
        )
    
    # Apply specific filters if provided
    if type_filter:
        query = query.filter(Masjid.type == type_filter)
    if madhab_filter:
        query = query.filter(Masjid.madhab == madhab_filter)
    if locale_filter:
        query = query.filter(Masjid.locale == locale_filter)
    
    # Get total count for pagination
    total = len(db.exec(query).all())
    total_pages = (total + size - 1) // size if total > 0 else 0
    
    # Apply pagination
    offset = (page - 1) * size
    query = query.offset(offset).limit(size)
    
    # Execute query
    masjids = db.exec(query).all()
    
    # Return paginated response
    return PaginatedMasjids(
        items=masjids,
        total=total,
        page=page,
        size=size,
        pages=total_pages
    )


def read_masjid(masjid_id: str, db: Session = Depends(get_session)):
    masjid = db.get(Masjid, masjid_id)
    if not masjid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Masjid not found with id: {masjid_id}",
        )
    return masjid


def update_masjid(masjid_id: str, masjid: MasjidUpdate, db: Session = Depends(get_session)):
    masjid_id = db.get(Masjid, masjid_id)
    if not masjid_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Masjid not found with id: {masjid_id}",
        )

    masjid_data = masjid.model_dump(exclude_unset=True)
    for key, value in masjid_data.items():
        setattr(masjid_id, key, value)

    db.add(masjid_id)
    db.commit()
    db.refresh(masjid_id)
    return masjid_id


def delete_masjid(masjid_id: int, db: Session = Depends(get_session)):
    masjid = db.get(Masjid, masjid_id)
    if not masjid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team not found with id: {masjid_id}",
        )

    db.delete(masjid)
    db.commit()
    return {"ok": True}
