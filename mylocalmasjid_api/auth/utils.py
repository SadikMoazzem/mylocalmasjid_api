from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import bcrypt
from sqlmodel import Session, select

from mylocalmasjid_api.auth.models import User, UserCreate, UserUpdate
from mylocalmasjid_api.database import get_session

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password: str, hashed_password: str):
    # encoding user password 
    userBytes = plain_password.encode('utf-8')

    hashBytes = hashed_password.encode('utf-8')
    
    # checking password 
    return bcrypt.checkpw(userBytes, hashBytes)


def get_password_hash(password: str):
    # converting password to array of bytes 
    bytes = password.encode('utf-8')
  
    # generating the salt 
    salt = bcrypt.gensalt() 
    
    # Hashing the password 
    return bcrypt.hashpw(bytes, salt).decode('utf-8')


def get_user(id: str,  db: Session = Depends(get_session)):
    user = db.get(User, id)
    print(user)
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

def get_available_users(user: User, db: Session = Depends(get_session)):
    if user.role == "admin":
        return db.exec(select(User)).all()
    else:
        return db.exec(select(User).where(User.related_masjid == user.related_masjid)).all()


def check_user_update_privileges(user: User, user_to_update_id: str):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User does not have permission to update user",
        )
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
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User does not have permission to update masjid",
        )
    # Admin can update any masjid
    if user.role == "admin":
        return True
    # Can only update own masjid
    elif str(user.related_masjid) == masjid_to_update_id:
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
    
    print(verify_password(password, user.hashed_password))
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
        related_masjid=validated_user.related_masjid,
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
    
    if not user.role == "admin":
        if user.role and user.role != user_to_update.role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User cannot change their role",
            )
        if user.related_masjid and user.related_masjid != user_to_update.related_masjid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User cannot change their masjid",
            )

    user_data = user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user_to_update, key, value)

    db.add(user_to_update)
    db.commit()
    db.refresh(user_to_update)
    return user_to_update