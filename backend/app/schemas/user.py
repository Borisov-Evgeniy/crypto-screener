from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True} #для pydantic разрешение парсить SQLAlchemy

class EmailUpdate(BaseModel):
    email: EmailStr

class PasswordUpdate(BaseModel):
    new_password: str

class StatusUpdate(BaseModel):
    is_active: bool



