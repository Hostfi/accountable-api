from sqlalchemy import text

from app.schemas.health import HealthResponse
from app.utils.redis import check_redis_health
from app.utils.supabase import check_supabase_health
from app.db.session import sessionmanager  # Import the session manager


async def check_db_connection() -> str:
    """Check the database connection using SQLAlchemy session."""
    try:
        async with sessionmanager.session() as session:
            # Execute a simple query to check the connection
            await session.execute(text("SELECT 1"))
        return "healthy"
    except Exception as e:
        print(f"Database connection check failed: {e}")  # Optional: log the error
        return "unhealthy"


class HealthService:
    async def check_health(self) -> HealthResponse:
        redis_status = await check_redis_health()
        supabase_status = await check_supabase_health()
        db_status = await check_db_connection()

        # Overall status is healthy only if all components are healthy
        all_statuses = [redis_status, supabase_status, db_status]
        overall_status = (
            "healthy"
            if all(status == "healthy" for status in all_statuses)
            else "degraded"
        )

        return HealthResponse(
            status=overall_status,
            redis_status=redis_status,
            supabase_status=supabase_status,
            db_status=db_status,
        )
