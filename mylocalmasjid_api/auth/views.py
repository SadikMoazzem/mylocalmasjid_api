from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from mylocalmasjid_api.auth.authenticate import (
    auth_access_wrapper,
    auth_refresh_wrapper,
    encode_login_token,
    encode_update_token,
)
from mylocalmasjid_api.auth.models import (
    AuthAccessToken,
    AuthRefreshToken,
    AuthTokens,
    UserCreate,
    UserLogin,
    UserPasswordReset,
    UserRead,
    UserUpdate,
)
from mylocalmasjid_api.auth.utils import (
    authenticate_user,
    change_user_password,
    check_user_update_privileges,
    create_new_user,
    get_user,
    get_available_users,
    update_user,
)
from mylocalmasjid_api.database import get_session
from mylocalmasjid_api.utils.logger import logger_config

router = APIRouter()

logger = logger_config(__name__)

# Standard login endpoint. Will return an access token and a refresh token
@router.post('/login', response_model=AuthTokens)
def login(
    user: UserLogin,
    db: Session = Depends(get_session)
):
    user = authenticate_user(user.email, user.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return encode_login_token(user=user)


@router.post('/refresh', response_model=AuthAccessToken)
def update_token(
    user=Depends(auth_refresh_wrapper)
):
    if user is None:
        raise HTTPException(status_code=401, detail="not authorization")
    return encode_update_token(user=user)


@router.get('/users', response_model=list[UserRead])
def get_users(
    user_request=Depends(auth_access_wrapper),
    db: Session = Depends(get_session)
):
    if not user_request:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    logger.info("%s.get_users: %s", __name__, user_request)
    current_user = get_user(user_request.id, db=db)
    available_users = get_available_users(current_user, db=db)

    return [UserRead.model_construct(**available_user.__dict__) for available_user in available_users]


# Get user endpoint. Will return current user
@router.get('/user', response_model=UserRead)
def get_current_user(
    user=Depends(auth_access_wrapper),
    db: Session = Depends(get_session)
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    logger.info("%s.get_current_user: %s", __name__, user)
    current_user = get_user(user.id, db=db)
    logger.info("%s.get_current_user: %s", __name__, current_user)

    return UserRead.model_construct(**current_user.__dict__)


# Update User
@router.put('/user/{user_id}', response_model=UserRead)
def update_a_user(
    user_id: str,
    user: UserUpdate,
    user_request=Depends(auth_access_wrapper),
    db: Session = Depends(get_session)
):
    check_user_update_privileges(user_request, user_id)
     
    updated_user = update_user(user_id, user, requesting_user=user_request, db=db)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error updating user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return updated_user


# Create User endpoint. Will return access token and refresh token
@router.post('/user')
def create_user(
    user: UserCreate,
    user_request=Depends(auth_access_wrapper),
    db: Session = Depends(get_session)):
    logger.info("%s.create_user: %s", __name__, user_request)
    if user_request.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authorized to create new user",
            headers={"WWW-Authenticate": "Bearer"},
        )

    create_new_user(user=user, db=db)
    return {"User Created": "Success"}


# Change password endpoint.
@router.put('/user/{user_id}/password-reset')
def change_a_password(
    user_id: str,
    change_obj: UserPasswordReset,
    user_request=Depends(auth_access_wrapper),
    db: Session = Depends(get_session)
):
    # TODO: Add code to check if user is allowed to change password for chosen user
    check_user_update_privileges(user_request, user_id)
    #

    if change_obj.new_password != change_obj.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Passwords do not match",
        )

    # Change password code goes here
    user = change_user_password(user_id, change_obj.new_password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error changing password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"Password update": "Success"}
