from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class OrganizationBase(BaseModel):
    name: str
    slug: str
    logo_url: Optional[str] = None
    billing_email: Optional[EmailStr] = None


class OrganizationCreate(OrganizationBase):
    plan: Optional[str] = "free"


class OrganizationUpdate(OrganizationBase):
    pass


class OrganizationInDB(OrganizationBase):
    id: UUID
    plan: str = "free"
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class OrganizationResponse(OrganizationInDB):
    pass


class OrganizationAdmin(BaseModel):
    organization_id: UUID
    user_id: UUID

    class Config:
        orm_mode = True
