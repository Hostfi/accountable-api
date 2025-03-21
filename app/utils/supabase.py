from supabase import create_client, Client

from app.core.config import settings


def get_supabase_client() -> Client:
    """Get a Supabase client instance."""
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


async def check_supabase_health() -> str:
    """Check Supabase connection health."""
    try:
        client = get_supabase_client()
        response = client.rpc("health_check").execute()
        if response:
            return response.data
    except Exception as e:
        return "unhealthy"

    return "unhealthy"
