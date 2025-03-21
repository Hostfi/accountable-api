from app.schemas.health import HealthResponse
from app.utils.redis import check_redis_health
from app.utils.supabase import check_supabase_health


class HealthService:
    async def check_health(self) -> HealthResponse:
        redis_status = await check_redis_health()
        supabase_status = await check_supabase_health()

        # Overall status is healthy only if all components are healthy
        overall_status = (
            "healthy"
            if all(status == "healthy" for status in [redis_status, supabase_status])
            else "degraded"
        )

        return HealthResponse(
            status=overall_status,
            redis_status=redis_status,
            supabase_status=supabase_status,
        )
