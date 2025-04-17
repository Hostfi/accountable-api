from __future__ import annotations

from typing import Any, Dict, Optional
from types import TracebackType
from clerk_backend_api import (
    AuthenticateRequestOptions,
    Clerk,
    RequestState,
    Requestish,
)
from fastapi import Request

from app.core.config import settings


class ClerkManager:
    """Manager for Clerk operations using the official SDK."""

    def __init__(self) -> None:
        self.client = Clerk(bearer_auth=settings.CLERK_SECRET_KEY)

    async def get_user(self, clerk_id: str) -> Optional[Dict[str, Any]]:
        """Get user data from Clerk."""
        try:
            response = await self.client.users.get_async(user_id=clerk_id)
            if not response:
                return None

            # Extract necessary user data
            email_obj = (
                next(
                    (email for email in response.email_addresses if email.id),
                    None,
                )
                if response.email_addresses
                else None
            )

            return {
                "clerk_id": response.id,
                "email": email_obj.email_address if email_obj else "",
                "first_name": response.first_name or "",
                "last_name": response.last_name or "",
                "avatar_url": response.profile_image_url,
            }

        except Exception as e:
            print(f"Error getting user from Clerk: {str(e)}")
            return None

    def __enter__(self) -> "ClerkManager":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        pass

    def authenticate_request(self, request: Request) -> RequestState:
        return self.client.authenticate_request(
            request,  # type: ignore[arg-type]
            AuthenticateRequestOptions(
                jwt_key=settings.CLERK_JWKS_KEY,
            ),
        )
