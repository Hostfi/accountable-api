from typing import Any, Dict, Optional, Tuple
from uuid import UUID

from app.managers.base_manager import BaseManager
from app.schemas.organization import OrganizationCreate, OrganizationUpdate


class OrganizationManager(BaseManager):
    """Manager for organization operations."""

    def __init__(self):
        super().__init__("organizations")

    async def create_organization(
        self, organization_create: OrganizationCreate, user_id: UUID
    ) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, str]]]:
        """Create a new organization with the given user as admin."""
        try:
            # Check if slug is already taken
            existing = await self.get_by_slug(organization_create.slug)
            if existing:
                return None, {"error": "Organization with this slug already exists"}

            # Create the organization
            org_data = organization_create.dict()
            organization = await self.create(org_data)

            if not organization:
                return None, {"error": "Failed to create organization"}

            # Set the user as the admin
            await self.client.table("organization_members").insert(
                {"organization_id": organization["id"], "user_id": str(user_id)}
            ).execute()

            return organization, None

        except Exception as e:
            return None, {"error": str(e)}

    async def get_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        """Get an organization by its slug."""
        result = (
            self.client.table(self.table_name).select("*").eq("slug", slug).execute()
        )
        if result.data and len(result.data) > 0:
            return result.data[0]
        return None

    async def update_organization(
        self, organization_id: UUID, organization_update: OrganizationUpdate
    ) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, str]]]:
        """Update an organization's details."""
        try:
            # Check if new slug is already taken (if slug is being updated)
            if organization_update.slug:
                existing = await self.get_by_slug(organization_update.slug)
                if existing and str(existing["id"]) != str(organization_id):
                    return None, {"error": "Organization with this slug already exists"}

            # Update the organization
            update_data = organization_update.dict(exclude_unset=True)
            organization = await self.update(organization_id, update_data)

            if not organization:
                return None, {"error": "Organization not found"}

            return organization, None

        except Exception as e:
            return None, {"error": str(e)}

    async def get_organization_admin(self, organization_id: UUID) -> Optional[UUID]:
        """Get the admin user ID for an organization."""
        result = (
            self.client.table("organization_members")
            .select("user_id")
            .eq("organization_id", str(organization_id))
            .execute()
        )
        if result.data and len(result.data) > 0:
            return UUID(result.data[0]["user_id"])
        return None
