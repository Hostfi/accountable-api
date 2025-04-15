from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    redis_status: str
    supabase_status: str
    db_status: str
    version: str = "1.0.0"
