from typing import Optional
from uuid import UUID

from fastapi import Depends, Header, HTTPException, status

from app.managers.user_manager import UserManager
from app.schemas.user import UserResponse


async def get_current_user(clerk_user_id: Optional[str] = Header(None)) -> UserResponse:
    """Get the current authenticated user."""
    if not clerk_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    user_manager = UserManager()
    user = await user_manager.get_user_by_clerk_id(clerk_user_id)

    if not user:
        # First time user, sync from Clerk
        user = await user_manager.sync_user_from_clerk(clerk_user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

    # Convert to UserResponse
    return UserResponse(
        id=UUID(user["id"]),
        clerk_id=user["clerk_id"],
        email=user["email"],
        full_name=user["full_name"],
        avatar_url=user.get("avatar_url", None),
        created_at=user["created_at"],
        updated_at=user["updated_at"],
    )
