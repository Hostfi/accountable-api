from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_current_user, verify_auth_request
from app.managers.user_manager import UserManager
from app.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/sync", response_model=UserResponse)
async def sync_user(
    clerk_id: str = Depends(verify_auth_request),
):
    """Sync user data from Clerk."""
    user_manager = UserManager()
    user = await user_manager.sync_user_from_clerk(clerk_id)

    if not user:
        raise HTTPException(status_code=400, detail="Failed to sync user")

    return user


@router.get("/me")
async def get_me(user: UserResponse = Depends(get_current_user)):
    return user
