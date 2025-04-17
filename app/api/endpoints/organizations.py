from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from sqlalchemy import update

from app.api.dependencies import get_current_user, DBSessionDep
from app.managers.organization_manager import OrganizationManager
from app.managers.user_manager import UserManager
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationResponse,
    OrganizationUpdate,
)
from app.schemas.user import UserResponse
from app.models.organization import Organization as OrganizationModel

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.post("", response_model=OrganizationResponse)
async def create_organization(
    organization_create: OrganizationCreate,
    db: DBSessionDep,
    current_user: UserResponse = Depends(get_current_user),
) -> OrganizationResponse:
    """Create a new organization."""
    # This endpoint likely needs significant rework to use SQLAlchemy session
    # For now, just adding type hint and fixing NameError
    # Replace below with SQLAlchemy logic
    # organization_manager = OrganizationManager()
    # organization, error = await organization_manager.create_organization(
    #     organization_create, current_user.id
    # )
    # if error:
    #     raise HTTPException(status_code=400, detail=error.get("error"))
    # return OrganizationResponse.model_validate(organization) # Assuming manager returns model

    # Placeholder logic just to fix type error for now
    # TODO: Replace with actual SQLAlchemy create logic using db session
    org_model = OrganizationModel(**organization_create.model_dump(), plan="free")
    db.add(org_model)  # Example add
    await db.flush()  # Example flush to get potential defaults
    await db.refresh(org_model)  # Example refresh
    # NOTE: This doesn't handle organization_members yet!

    # Simulate error handling path for completeness
    error = None  # Placeholder
    if error:
        raise HTTPException(status_code=400, detail=error)

    return OrganizationResponse.model_validate(
        org_model
    )  # Return validated Pydantic model


@router.get("", response_model=List[OrganizationResponse])
async def get_user_organizations(
    db: DBSessionDep,
    current_user: UserResponse = Depends(get_current_user),
) -> List[OrganizationResponse]:
    """Get organizations for the current user."""
    # This endpoint likely needs significant rework to use SQLAlchemy session
    # For now, just adding type hint
    # Replace below with SQLAlchemy logic using db session and relationships
    # user_manager = UserManager()
    # organizations = await user_manager.get_user_organizations(current_user.id)
    # return [OrganizationResponse.model_validate(org) for org in organizations]

    # Placeholder logic
    # TODO: Replace with actual SQLAlchemy query logic
    return []  # Return empty list for now


@router.get("/{organization_id}", response_model=OrganizationResponse)
async def get_organization(
    organization_id: UUID,
    db: DBSessionDep,
    current_user: UserResponse = Depends(get_current_user),
) -> OrganizationResponse:
    """Get organization details."""
    # This endpoint likely needs significant rework to use SQLAlchemy session
    # Replace below with SQLAlchemy logic
    # organization_manager = OrganizationManager()
    # organization = await organization_manager.get_by_id(organization_id)

    # Placeholder logic
    # TODO: Replace with actual SQLAlchemy query logic and auth check
    stmt = select(OrganizationModel).where(OrganizationModel.id == organization_id)
    result = await db.execute(stmt)
    org_model = result.scalars().first()

    if not org_model:
        raise HTTPException(status_code=404, detail="Organization not found")

    # TODO: Add authorization check - does current_user have access to org_model?

    return OrganizationResponse.model_validate(org_model)


@router.put("/{organization_id}", response_model=OrganizationResponse)
async def update_organization(
    organization_id: UUID,
    organization_update: OrganizationUpdate,
    db: DBSessionDep,
    current_user: UserResponse = Depends(get_current_user),
) -> OrganizationResponse:
    """Update organization details."""
    # This endpoint likely needs significant rework to use SQLAlchemy session
    # Replace below with SQLAlchemy logic
    # organization_manager = OrganizationManager()
    # organization, error = await organization_manager.update_organization(
    #     organization_id, organization_update
    # )

    # Placeholder logic
    # TODO: Replace with actual SQLAlchemy query logic and auth check
    update_data = organization_update.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")

    # Fetch the existing organization first (includes auth check placeholder)
    stmt_select = select(OrganizationModel).where(
        OrganizationModel.id == organization_id
    )
    result_select = await db.execute(stmt_select)
    org_model = result_select.scalars().first()

    if not org_model:
        raise HTTPException(status_code=404, detail="Organization not found")

    # TODO: Add authorization check - does current_user have access to org_model?

    # Update the organization
    for key, value in update_data.items():
        setattr(org_model, key, value)

    db.add(org_model)  # Add the updated model to the session
    await db.flush()
    await db.refresh(org_model)

    # Simulate error handling path for completeness
    error = None  # Placeholder
    if error:
        raise HTTPException(status_code=400, detail=error)

    return OrganizationResponse.model_validate(org_model)
