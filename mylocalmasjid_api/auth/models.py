import enum
import uuid
from typing import Optional

from pydantic import BaseModel
from sqlmodel import Column, Enum, Field, SQLModel


class UserRole(str, enum.Enum):
    admin = "admin"
    masjid_admin = "masjid_admin"

class UserBase(SQLModel):
    __tablename__ = 'users'

    email: str
    role: UserRole = Column(Enum(UserRole), default=UserRole.masjid_admin)
    active: bool
    full_name: Optional[str]
    related_masjid: Optional[uuid.UUID] = Field(foreign_key="masjids.id", nullable=True)


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str


class UserRead(UserBase):
    id: uuid.UUID


class UserUpdate(UserBase):
    pass


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserPasswordReset(BaseModel):
    new_password: str
    confirm_password: str


class AuthRefreshToken(BaseModel):
    refresh_token: str
