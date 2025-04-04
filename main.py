import logging
import time

from dotenv import load_dotenv
import uvicorn
from fastapi import Depends, FastAPI
from fastapi_limiter.depends import RateLimiter

from app.api.endpoints import health, organizations, users
from app.core.config import settings
from app.utils.redis import init_redis

app = FastAPI(dependencies=[Depends(RateLimiter(times=20, seconds=10))])
logger = logging.getLogger(__name__)
# .env variables can be validated and accessed from the config, here to set a log level
logging.basicConfig(level=settings.LOG_LEVEL.upper())


# Register routers
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


@app.on_event("startup")
async def startup():
    await init_redis()


def dev():
    load_dotenv(".env.local", override=True)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
