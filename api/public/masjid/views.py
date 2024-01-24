from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from api.database import get_session
from api.public.announcement import views as announcement_api
from api.public.facility import views as facility_api
from api.public.location import views as location_api
from api.public.masjid.crud import create_masjid, read_masjid, read_masjids, update_masjid
from api.public.masjid.models import MasjidCreate, MasjidRead, MasjidUpdate
from api.public.prayer_times import views as prayer_times_api
from api.public.special_prayer import views as special_prayers_api
from api.utils.logger import logger_config

router = APIRouter()

logger = logger_config(__name__)


@router.get("", response_model=list[MasjidRead])
def get_masjids(
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    db: Session = Depends(get_session),
):
    logger.info("%s.get_masjids: triggered", __name__)
    return read_masjids(offset=offset, limit=limit, db=db)


@router.get("/{masjid_id}", response_model=MasjidRead)
def get_a_masjid(masjid_id: str, db: Session = Depends(get_session)):
    logger.info("%s.get_a_masjid.id: %s", __name__, masjid_id)
    return read_masjid(masjid_id=masjid_id, db=db)


@router.patch("/{masjid_id}", response_model=MasjidUpdate)
def update_a_masjid(masjid_id: str, masjid: MasjidUpdate, db: Session = Depends(get_session)):
    logger.info("%s.update_a_masjid.id: %s", __name__, masjid_id)
    return update_masjid(masjid_id=masjid_id, masjid=masjid, db=db)


@router.post("", response_model=MasjidRead)
def create_a_masjid(masjid: MasjidCreate, db: Session = Depends(get_session)):
    logger.info("%s.create_a_masjid: %s", __name__, masjid)
    return create_masjid(masjid=masjid, db=db)


# @router.delete("/{masjid_id}")
# def delete_a_masjid(masjid_id: str, db: Session = Depends(get_session)):
#     logger.info("%s.delete_a_masjid: %s triggered", __name__, masjid_id)
#     return delete_masjid(masjid_id=masjid_id, db=db)

router.include_router(
    prayer_times_api.router,
    prefix="/{masjid_id}/prayer_times",
    # tags=["prayer_times"],
    responses={404: {"description": "Not found"}},
    # middleware=[],
)

router.include_router(
    location_api.router,
    prefix="/{masjid_id}/location",
    # tags=["location"],
    responses={404: {"description": "Not found"}},
)

router.include_router(
    announcement_api.router,
    prefix="/{masjid_id}/announcement",
    # tags=["announcement"],
    responses={404: {"description": "Not found"}},
)

router.include_router(
    facility_api.router,
    prefix="/{masjid_id}/facility",
    # tags=["facility"],
    responses={404: {"description": "Not found"}},
)

router.include_router(
    special_prayers_api.router,
    prefix="/{masjid_id}/special_prayers",
    # tags=["special_prayers"],
    responses={404: {"description": "Not found"}},
)
