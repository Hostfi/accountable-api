from typing import Optional
from uuid import UUID

from app.managers.user_manager import UserManager
from app.schemas.user import UserResponse


class UserService:
    """Service for user-related operations."""

    def __init__(self) -> None:
        self.user_manager = UserManager()

    async def get_user(self, clerk_id: str) -> Optional[UserResponse]:
        """Get an existing user by Clerk ID."""
        try:
            user = await self.user_manager.get_user_by_clerk_id(clerk_id)
            if not user:
                return None

            return UserResponse(
                id=UUID(user["id"]),
                clerk_id=user["clerk_id"],
                email=user["email"],
                first_name=user.get("first_name"),
                last_name=user.get("last_name"),
                avatar_url=user.get("avatar_url"),
                created_at=user["created_at"],
                updated_at=user["updated_at"],
            )

        except Exception as e:
            print(f"Error getting user: {str(e)}")
            return None
