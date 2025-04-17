from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from clerk_backend_api import RequestState

from app.managers.clerk_manager import ClerkManager
from app.schemas.user import UserResponse
from app.services.user import UserService
from app.db.session import get_db_session


DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]


async def verify_auth_request(
    request: Request,
) -> str:
    """Verify the request authentication using Clerk. Returns Clerk User ID."""
    try:
        clerk_manager = ClerkManager()
        auth: RequestState = clerk_manager.authenticate_request(request)
        if not auth.is_signed_in or not auth.payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not signed in or payload missing",
            )

        clerk_id: str | None = auth.payload.get("sub")
        if not clerk_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Clerk User ID (sub) missing from token payload",
            )
        return clerk_id

    except Exception as e:
        print(f"Authentication failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
        )


async def get_current_user(
    db: DBSessionDep,
    clerk_id: str = Depends(verify_auth_request),
) -> UserResponse:
    """Get the current authenticated user from DB using Clerk ID."""
    user_service = UserService()
    user = await user_service.get_user(clerk_id=clerk_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found in database",
        )

    return user
