from app.schemas.health import HealthResponse
from app.utils.redis import check_redis_health


class HealthService:
    async def check_health(self) -> HealthResponse:
        redis_status = await check_redis_health()
        return HealthResponse(
            status="healthy",
            redis_status=redis_status,
        )
