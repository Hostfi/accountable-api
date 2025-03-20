from fastapi import APIRouter

from app.schemas.health import HealthResponse
from app.services.health import HealthService

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    health_service = HealthService()
    return await health_service.check_health()
