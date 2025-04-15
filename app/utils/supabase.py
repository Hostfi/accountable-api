from supabase import create_client, Client

from app.core.config import settings


def get_supabase_client() -> Client:
    """Get a Supabase client instance."""
    return create_client(
        f"https://{settings.SUPABASE_PROJECT_ID}.supabase.co",
        settings.SUPABASE_KEY,
    )


async def check_supabase_health() -> str:
    """Check Supabase connection health."""
    try:
        get_supabase_client()
        return "healthy"
    except Exception as e:
        return "unhealthy"
