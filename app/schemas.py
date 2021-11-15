from typing import Optional

from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    create_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class SerialS(BaseModel):
    name: str
    description: str
    #photo: str
    owner_id : int


class EpisodeS(BaseModel):
    name: str
    description: str


class EpisodeCreate(EpisodeS):
    name: str
    description: str
    serial_id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
