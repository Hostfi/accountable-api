from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_current_user
from app.managers.organization_manager import OrganizationManager
from app.managers.user_manager import UserManager
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationResponse,
    OrganizationUpdate,
)
from app.schemas.user import UserResponse

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.post("", response_model=OrganizationResponse)
async def create_organization(
    organization_create: OrganizationCreate,
    current_user: UserResponse = Depends(get_current_user),
):
    """Create a new organization."""
    print(organization_create)
    # organization_manager = OrganizationManager()
    # organization, error = await organization_manager.create_organization(
    #     organization_create, current_user.id
    # )

    # if error:
    #     raise HTTPException(status_code=400, detail=error.get("error"))

    return organization


@router.get("", response_model=List[OrganizationResponse])
async def get_user_organizations(
    current_user: UserResponse = Depends(get_current_user),
):
    """Get organizations for the current user."""
    user_manager = UserManager()
    organizations = await user_manager.get_user_organizations(current_user.id)
    return organizations


@router.get("/{organization_id}", response_model=OrganizationResponse)
async def get_organization(
    organization_id: UUID,
    current_user: UserResponse = Depends(get_current_user),
):
    """Get organization details."""
    organization_manager = OrganizationManager()
    organization = await organization_manager.get_by_id(organization_id)

    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    return organization


@router.put("/{organization_id}", response_model=OrganizationResponse)
async def update_organization(
    organization_id: UUID,
    organization_update: OrganizationUpdate,
    current_user: UserResponse = Depends(get_current_user),
):
    """Update organization details."""
    organization_manager = OrganizationManager()
    organization, error = await organization_manager.update_organization(
        organization_id, organization_update
    )

    if error:
        raise HTTPException(status_code=400, detail=error.get("error"))

    return organization
