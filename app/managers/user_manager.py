from typing import Any, Dict, List, Optional
from uuid import UUID


from app.managers.base_manager import BaseManager
from app.managers.clerk_manager import ClerkManager
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserManager(BaseManager[User]):
    """Manager for user operations."""

    def __init__(self) -> None:
        super().__init__("users")

    async def get_user_by_clerk_id(self, clerk_id: str) -> Optional[Dict[str, Any]]:
        """Get a user by their Clerk ID."""
        result = (
            self.client.table(self.table_name)
            .select("*")
            .eq("clerk_id", clerk_id)
            .execute()
        )
        if result.data and len(result.data) > 0:
            return result.data[0]
        return None

    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get a user by their email."""
        result = (
            self.client.table(self.table_name).select("*").eq("email", email).execute()
        )
        if result.data and len(result.data) > 0:
            return result.data[0]
        return None

    async def sync_user_from_clerk(self, clerk_id: str) -> Optional[Dict[str, Any]]:
        """Sync user data from Clerk to Supabase."""
        try:
            # Get user data from Clerk using ClerkManager
            with ClerkManager() as clerk:
                clerk_user = await clerk.get_user(clerk_id)
                if not clerk_user:
                    return None

                # Check if user already exists in Supabase
                existing_user = await self.get_user_by_clerk_id(clerk_id)

                if existing_user:
                    # Update user if exists
                    user_data = {
                        "email": clerk_user["email"],
                        "first_name": clerk_user["first_name"],
                        "last_name": clerk_user["last_name"],
                        "avatar_url": clerk_user["avatar_url"],
                    }
                    return await self.update(UUID(existing_user["id"]), user_data)
                else:
                    # Create new user
                    return await self.create(clerk_user)

        except Exception as e:
            print(f"Error syncing user from Clerk: {str(e)}")
            return None

    async def create_user(self, user_create: UserCreate) -> Optional[Dict[str, Any]]:
        """Create a new user in Supabase."""
        try:
            # First check if user already exists
            existing_user = await self.get_user_by_clerk_id(user_create.clerk_id)
            if existing_user:
                return existing_user

            # Create user in Supabase
            user_data = user_create.dict()
            return await self.create(user_data)

        except Exception as e:
            print(f"Error creating user: {str(e)}")
            return None

    async def update_user(
        self, user_id: UUID, user_update: UserUpdate
    ) -> Optional[Dict[str, Any]]:
        """Update a user in Supabase."""
        try:
            # Create update data, removing None values
            update_data = {k: v for k, v in user_update.dict().items() if v is not None}
            if not update_data:
                return await self.get_by_id(user_id)

            return await self.update(user_id, update_data)

        except Exception as e:
            print(f"Error updating user: {str(e)}")
            return None

    async def get_user_organizations(self, user_id: UUID) -> List[Dict[str, Any]]:
        """Get all organizations a user administers."""
        result = self.client.rpc(
            "get_user_organizations", {"user_id_param": str(user_id)}
        ).execute()
        return result.data if result.data else []
