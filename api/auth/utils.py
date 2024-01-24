from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlmodel import Session, select

from api.auth.models import User, UserCreate, UserUpdate
from api.database import get_session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(id: str,  db: Session = Depends(get_session)):
    user = db.get(User, id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found with id: {id}",
        )
    
    if user.active is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User is disabled",
        )

    return user


def check_user_update_privileges(user: User, user_to_update_id: str):
    # Admin can update any user
    if user.role == "admin":
        return True
    # Can onlt update own user
    elif str(user.id) == user_to_update_id:
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User does not have permission to update user",
        )


def check_user_masjid_update_privileges(user: User, masjid_to_update_id: str):
    # Admin can update any masjid
    if user.role == "admin":
        return True
    # Can only update own masjid
    elif str(user.masjid_id) == masjid_to_update_id:
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User does not have permission to update masjid",
        )



def authenticate_user(email: str, password: str, db: Session = Depends(get_session)):
    user = db.exec(select(User).where(User.email == email)).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    if user.active is False:
        return False
    return user


# User CRUD
def create_new_user(user: UserCreate, db: Session = Depends(get_session)):
    validated_user = UserCreate.model_validate(user)
    existing_user = db.exec(select(User).where(User.email == validated_user.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email is in use",
        )
    user_to_add = User(
        email=validated_user.email,
        full_name=validated_user.full_name,
        masjid_id=validated_user.masjid_id,
        hashed_password=get_password_hash(validated_user.password),
        active=True,
        role=validated_user.role,
    )
    db.add(user_to_add)
    db.commit()
    db.refresh(user_to_add)
    return user_to_add


def change_user_password(id: str, password: str, db: Session = Depends(get_session)):
    user = get_user(id, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found with id: {id}",
        )

    user.hashed_password = get_password_hash(password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(id: str, user: UserUpdate, db: Session = Depends(get_session)):
    UserUpdate.model_validate(user)

    user_to_update = get_user(id, db=db)
    if not user_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found with id: {id}",
        )

    user_data = user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user_to_update, key, value)

    db.add(user_to_update)
    db.commit()
    db.refresh(user_to_update)
    return user_to_update