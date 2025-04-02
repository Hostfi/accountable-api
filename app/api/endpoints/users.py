import asyncio

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache

from app.api.dependencies import get_current_user
from app.managers.user_manager import UserManager
from app.schemas.user import UserCreate, UserResponse
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/user", response_model=UserResponse)
def current_user() -> UserResponse:
    user_service = UserService()
    return user_service.get_current_user()


@router.get("/cached", response_model=UserResponse)
@cache(expire=30)
async def cached_user() -> UserResponse:
    # Simulate slow operation
    await asyncio.sleep(5)
    user_service = UserService()
    return await user_service.get_cached_user()


@router.post("/sync", response_model=UserResponse)
async def sync_user(
    user_data: UserCreate,
    current_user: UserResponse = Depends(get_current_user),
):
    """Sync user data from Clerk."""
    # Validate that the request is for the authenticated user
    if user_data.clerk_id != current_user.clerk_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    user_manager = UserManager()
    user = await user_manager.sync_user_from_clerk(user_data.clerk_id)

    if not user:
        raise HTTPException(status_code=400, detail="Failed to sync user")

    return user
