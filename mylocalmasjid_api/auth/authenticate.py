from datetime import datetime, timedelta
from json import loads
from types import SimpleNamespace

import jwt
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import exceptions
from sqlmodel import Session

from mylocalmasjid_api.auth.models import User
from mylocalmasjid_api.auth.utils import get_user
from mylocalmasjid_api.config import settings
from mylocalmasjid_api.database import get_session
from mylocalmasjid_api.utils.logger import logger_config

security = HTTPBearer()

secret = settings.SECRET_KEY
access_token_expire = settings.ACCESS_TOKEN_EXPIRE
refresh_token_expire = settings.REFRESH_TOKEN_EXPIRE

logger = logger_config(__name__)

def encode_token(user: User, type: str):
    payload = dict(
        iss = user.model_dump_json(),
        sub = type
    )
    to_encode = payload.copy()
    if type == "access_token":
        to_encode.update({"exp": datetime.utcnow() + timedelta(seconds=access_token_expire)})
    else:
        to_encode.update({"exp": datetime.utcnow() + timedelta(seconds=refresh_token_expire)})

    return jwt.encode(to_encode, secret, algorithm='HS256')

def encode_login_token(user: User):
    access_token = encode_token(user=user, type="access_token")
    refresh_token = encode_token(user=user, type="refresh_token")

    login_token = dict(
        access_token=f"{access_token}",
        refresh_token=f"{refresh_token}"
    ) 
    return login_token

def encode_update_token(user: User):
    access_token = encode_token(user=user, type="access_token")

    update_token = dict(
        access_token=f"{access_token}"
    ) 
    return update_token


def decode_access_token(token: str) -> User:
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        if payload['sub'] != "access_token":
            raise HTTPException(status_code=401, detail='Invalid token')
        json_t= loads(payload['iss'], object_hook=lambda d: SimpleNamespace(**d))
        logger.info("%s.decode_access_token: %s", __name__, json_t)
        return User.model_validate(json_t, from_attributes=True)
    except exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Signature has expired')
    except exceptions.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail='Invalid token')

def decode_refresh_token(token) -> User:
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        if payload['sub'] != "refresh_token":
            raise HTTPException(status_code=401, detail='Invalid token')
        json_t= loads(payload['iss'], object_hook=lambda d: SimpleNamespace(**d))
        return User.model_validate(json_t, from_attributes=True)
    except exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Signature has expired')
    except exceptions.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail='Invalid token')


def auth_access_wrapper(
        auth: HTTPAuthorizationCredentials = Security(security),
        db: Session = Depends(get_session)
    ):
    user_obj = decode_access_token(auth.credentials)
    user = get_user(user_obj.id, db=db)
    return user



def auth_refresh_wrapper(auth: HTTPAuthorizationCredentials = Security(security)):
    return decode_refresh_token(auth.credentials)