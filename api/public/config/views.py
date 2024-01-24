from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session

from api.database import get_session
from api.public.config.crud import get_config, update_config_option, add_config_option
from api.public.config.models import Config, ConfigCreate
from api.utils.logger import logger_config

from api.auth.authenticate import auth_access_wrapper

router = APIRouter()

logger = logger_config(__name__)


@router.get("", response_model=Config)
def get_all_options(db: Session = Depends(get_session)):
    logger.info("%s.get_all_options: %s", __name__)
    return get_config(db=db)


@router.patch("/{config_id}", response_model=ConfigCreate)
def update_config(
    config_id: str,
    config: Config,
    db: Session = Depends(get_session),
    user_request=Depends(auth_access_wrapper),
):
    # logger.info("%s.update_config_option: %s", __name__, config)
    logger.info("%s.update_config_option [ID]: %s", __name__, user_request)
    if not user_request.role == "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User not authorized to update config option",
        )
    return update_config_option(id=config_id, config=config, db=db)


@router.post("", response_model=ConfigCreate)
def create_a_config(
    config: Config,
    db: Session = Depends(get_session),
    user_request=Depends(auth_access_wrapper),
):
    logger.info("%s.create_a_config: %s", __name__, config)
    if not user_request.role == "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User not authorized to create config option",
        )
    return add_config_option(config_option=config, db=db)