from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, ConfigDict


class OrganizationBase(BaseModel):
    name: str | None = None
    logo_url: Optional[str] = None
    website_url: Optional[str] = None
    billing_email: Optional[EmailStr] = None
    ein: Optional[str] = None
    plan: Optional[str] = None


class OrganizationCreate(OrganizationBase):
    name: str
    plan: Optional[str] = "free"


class OrganizationUpdate(OrganizationBase):
    pass


class OrganizationResponse(OrganizationBase):
    id: UUID
    plan: str
    created_at: datetime
    updated_at: datetime
    name: str

    model_config = ConfigDict(from_attributes=True)


class OrganizationAdmin(BaseModel):
    organization_id: UUID
    user_id: UUID

    model_config = ConfigDict(from_attributes=True)
