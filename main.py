import logging
import time
import contextlib

from dotenv import load_dotenv
import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter.depends import RateLimiter

from app.api.endpoints import health, organizations, users
from app.core.config import settings
from app.utils.redis import init_redis
from app.db.session import sessionmanager


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    await init_redis()
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()


app = FastAPI(
    lifespan=lifespan, dependencies=[Depends(RateLimiter(times=20, seconds=10))]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=settings.LOG_LEVEL.upper())


app.include_router(health.router)
app.include_router(users.router)
app.include_router(organizations.router)


@app.middleware("http")
async def time_request(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["Server-Timing"] = str(process_time)
    logger.info(f"{request.method} {round(process_time, 5)}s {request.url}")
    return response


def dev():
    load_dotenv(".env.local", override=True)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
