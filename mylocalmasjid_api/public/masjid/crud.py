from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select

from mylocalmasjid_api.database import get_session
from mylocalmasjid_api.public.masjid.models import Masjid, MasjidCreate, MasjidUpdate


def create_masjid(masjid: MasjidCreate, db: Session = Depends(get_session)):
    masjid_to_db = Masjid.model_validate(masjid)
    db.add(masjid_to_db)
    db.commit()
    db.refresh(masjid_to_db)
    return masjid_to_db


def read_masjids(offset: int = 0, limit: int = 20, db: Session = Depends(get_session)):
    masjids = db.exec(select(Masjid).offset(offset).limit(limit)).all()
    print(masjids)
    return masjids


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
