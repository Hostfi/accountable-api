from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
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
    @property
    def full_name(self) -> str:
        """Get the user's full name."""
        return f"{self.first_name or ''} {self.last_name or ''}".strip() or None
