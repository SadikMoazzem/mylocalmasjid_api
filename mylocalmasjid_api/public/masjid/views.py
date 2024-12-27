from fastapi import APIRouter, Depends, Query,  HTTPException, status
from sqlmodel import Session
from typing import Optional

from mylocalmasjid_api.database import get_session
from mylocalmasjid_api.public.announcement import views as announcement_api
from mylocalmasjid_api.public.facility import views as facility_api
from mylocalmasjid_api.public.location import views as location_api
from mylocalmasjid_api.public.masjid.crud import create_masjid, read_masjid, read_masjids, update_masjid
from mylocalmasjid_api.public.masjid.models import MasjidCreate, MasjidRead, MasjidUpdate, PaginatedMasjids
from mylocalmasjid_api.public.prayer_times import views as prayer_times_api
from mylocalmasjid_api.public.special_prayer import views as special_prayers_api
from mylocalmasjid_api.utils.logger import logger_config

from mylocalmasjid_api.auth.authenticate import auth_access_wrapper
from mylocalmasjid_api.auth.utils import check_user_masjid_update_privileges

router = APIRouter()

logger = logger_config(__name__)


@router.get("", response_model=PaginatedMasjids)
def get_masjids(
    search: str = "",
    type_filter: Optional[str] = None,
    madhab_filter: Optional[str] = None,
    locale_filter: Optional[str] = None,
    page: int = Query(default=1, gt=0),
    size: int = Query(default=20, gt=0, le=100),
    db: Session = Depends(get_session),
    user_request=Depends(auth_access_wrapper),
):
    logger.info("%s.get_masjids: triggered", __name__)
    # If user is not authenticated, pass None to read_masjids
    if not user_request:
        user_request = None
    
    return read_masjids(
        search=search,
        type_filter=type_filter,
        madhab_filter=madhab_filter,
        locale_filter=locale_filter,
        page=page,
        size=size,
        db=db,
        user=user_request
    )


@router.get("/masjid/{masjid_id}", response_model=MasjidRead)
def get_a_masjid(
    masjid_id: str, 
    db: Session = Depends(get_session),
    user_request=Depends(auth_access_wrapper),
):
    logger.info("%s.get_a_masjid.id: %s", __name__, masjid_id)
    
    # If user is not authenticated, return 401
    if not user_request:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    
    # If user is admin, they can see any masjid
    if user_request.role == "admin":
        return read_masjid(masjid_id=masjid_id, db=db)
    
    # If user is masjid_admin, they can only see their assigned masjid
    if user_request.role == "masjid_admin":
        if str(user_request.related_masjid) != masjid_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this masjid",
            )
        return read_masjid(masjid_id=masjid_id, db=db)
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not authorized to view masjids",
    )


@router.patch("/masjid/{masjid_id}", response_model=MasjidUpdate)
def update_a_masjid(
    masjid_id: str,
    masjid: MasjidUpdate,
    db: Session = Depends(get_session),
    user_request=Depends(auth_access_wrapper),
):
    logger.info("%s.update_a_masjid.id: %s", __name__, masjid_id)
    check_user_masjid_update_privileges(user_request, masjid_id)
    return update_masjid(masjid_id=masjid_id, masjid=masjid, db=db)


@router.post("/masjid", response_model=MasjidRead)
def create_a_masjid(
    masjid: MasjidCreate,
    db: Session = Depends(get_session),
    user_request=Depends(auth_access_wrapper),
):
    logger.info("%s.create_a_masjid: %s", __name__, masjid)
    if not user_request:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User not authorized to create masjid",
        )
    
    # Only admin can create masjid
    if not user_request.role == "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User not authorized to create masjid",
        )
    return create_masjid(masjid=masjid, db=db)


# @router.delete("/{masjid_id}")
# def delete_a_masjid(masjid_id: str, db: Session = Depends(get_session)):
#     logger.info("%s.delete_a_masjid: %s triggered", __name__, masjid_id)
#     return delete_masjid(masjid_id=masjid_id, db=db)

router.include_router(
    prayer_times_api.router,
    prefix="/masjid/{masjid_id}/prayer-times",
    # tags=["prayer_times"],
    responses={404: {"description": "Not found"}},
    # middleware=[],
)

router.include_router(
    location_api.router,
    prefix="/masjid/{masjid_id}/location",
    # tags=["location"],
    responses={404: {"description": "Not found"}},
)

router.include_router(
    announcement_api.router,
    prefix="/masjid/{masjid_id}/announcement",
    # tags=["announcement"],
    responses={404: {"description": "Not found"}},
)

router.include_router(
    facility_api.router,
    prefix="/masjid/{masjid_id}/facility",
    # tags=["facility"],
    responses={404: {"description": "Not found"}},
)

router.include_router(
    special_prayers_api.router,
    prefix="/masjid/{masjid_id}/special-prayers",
    # tags=["special_prayers"],
    responses={404: {"description": "Not found"}},
)
