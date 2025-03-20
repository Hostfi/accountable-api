import asyncio

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.schemas.user import UserResponse
from app.services.user import UserService

router = APIRouter()


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
