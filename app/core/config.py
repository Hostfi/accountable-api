from typing import List, Union, Any

from dotenv import load_dotenv
from pydantic import field_validator
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://local.tryaccountable.ai:3000",
        "*.tryaccountable.ai",
    ]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Redis settings
    REDISHOST: str = "localhost"
    REDISPORT: str = "6379"
    REDISUSER: str = ""
    REDISPASSWORD: str = ""

    @field_validator("REDISHOST", "REDISPORT")
    @classmethod
    def check_redis(cls, v: Any, field: Any) -> Any:
        if not v:
            raise ValueError(
                f"{field.name} must be defined. For local development, you can use the default value in your .env '{field.name}={field.default}'"
            )
        return v

    # Supabase settings
    SUPABASE_KEY: str
    SUPABASE_DB_PASSWORD: str
    SUPABASE_PROJECT_ID: str
    SUPABASE_ACCESS_TOKEN: str
    DATABASE_URL: str

    # Clerk settings
    NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY: str
    CLERK_SECRET_KEY: str
    CLERK_JWKS_KEY: str

    # OpenAI settings
    OPENAI_API_KEY: str

    # Logging
    LOG_LEVEL: str = "info"

    @field_validator("LOG_LEVEL")
    @classmethod
    def check_log_level(cls, v: str, field: Any) -> str:
        if v not in ["debug", "info", "warning", "error", "critical"]:
            raise ValueError(
                f"{field.name} must be a standard log level. For local development, you can use the default value in your .env '{field.name}={field.default}'"
            )
        return v

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()  # type: ignore[call-arg] # Ignore MyPy error for missing env vars
