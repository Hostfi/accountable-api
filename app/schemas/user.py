from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None


class UserCreate(UserBase):
    clerk_id: str


class UserUpdate(UserBase):
    pass


class UserInDB(UserBase):
    id: UUID
    clerk_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserResponse(UserInDB):
    pass
