from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select

from api.database import get_session
from api.public.config.models import Config, ConfigCreate


def get_config(db: Session = Depends(get_session)):
    config_options = db.exec(select(Config)).all()
    if not config_options:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Config Options not found",
        )
    return [config_option.model_dump() for config_option in config_options]


def update_config_option(id: str, config: ConfigCreate, db: Session = Depends(get_session)):
    config_option_to_update = db.exec(select(Config).where(Config.id == id)).first()
    if not config_option_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Config Option not found with id: {id}",
        )
    ConfigCreate.model_validate(config)
    config_option_data = config.model_dump(exclude_unset=True)
    for key, value in config_option_data.items():
        setattr(config_option_to_update, key, value)

    db.add(config_option_to_update)
    db.commit()
    db.refresh(config_option_to_update)
    return config_option_to_update


def add_config_option(config_option: ConfigCreate, db: Session = Depends(get_session)):
    ConfigCreate.model_validate(config_option)
    config_option_to_add = Config(**config_option.model_dump())
    db.add(config_option_to_add)
    db.commit()
    db.refresh(config_option_to_add)
    return config_option_to_add
