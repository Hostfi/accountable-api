from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, ConfigDict


# Base schema reflecting common user fields
class UserBase(BaseModel):
    email: EmailStr | None = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None


# Schema for creating a user (likely based on Clerk data)
# Needs clerk_id and email at minimum
class UserCreate(UserBase):
    clerk_id: str
    email: EmailStr


# Schema for updating a user (all fields optional)
class UserUpdate(UserBase):
    pass


# Schema for representing user data in API responses
class UserResponse(UserBase):
    id: UUID
    clerk_id: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @property
    def full_name(self) -> str | None:
        """Get the user's full name."""
        if self.first_name or self.last_name:
            return f"{self.first_name or ''} {self.last_name or ''}".strip()
        return None
