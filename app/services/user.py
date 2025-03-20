from app.schemas.user import UserResponse


class UserService:
    def get_current_user(self) -> UserResponse:
        return UserResponse(
            user_id="0123456789",
            email="me@kylegill.com",
            name="Kyle Gill",
        )

    async def get_cached_user(self) -> UserResponse:
        return UserResponse(
            user_id="0123456789",
            email="cached@kylegill.com",
            name="Kyle Gill",
        )
