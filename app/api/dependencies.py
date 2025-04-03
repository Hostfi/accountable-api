from typing import Optional, Tuple
from uuid import UUID

from fastapi import Depends, Request, HTTPException, status
from clerk_backend_api import RequestState

from app.core.config import settings
from app.managers.clerk_manager import ClerkManager
from app.managers.user_manager import UserManager
from app.schemas.user import UserResponse
from app.services.user import UserService


async def verify_auth_request(
    request: Request,
) -> str:
    """Verify the request authentication using Clerk."""
    try:
        # Initialize Clerk manager
        clerk_manager = ClerkManager()

        # Authenticate the request
        auth: RequestState = clerk_manager.authenticate_request(request)
        if not auth.is_signed_in:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not signed in",
            )

        return auth.payload["sub"]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}",
        )


async def get_current_user(
    clerk_id: str = Depends(verify_auth_request),
) -> UserResponse:
    """Get the current authenticated user."""
    user_service = UserService()
    user = await user_service.get_user(clerk_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found in database",
        )

    return user
