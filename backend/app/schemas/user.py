from typing import Optional

from app.schemas.core import CoreModel


class UserBase(CoreModel):
    email: str
    nickname: str
    full_name: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserResponse(UserBase):
    id: int


class UserAssitant(CoreModel):
    id: int
    full_name: str
