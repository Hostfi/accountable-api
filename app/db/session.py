import contextlib
from typing import Any, AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

# Ensure DATABASE_URL is set and uses the asyncpg driver
if not settings.DATABASE_URL or not settings.DATABASE_URL.startswith(
    "postgresql+asyncpg"
):
    raise ValueError(
        "DATABASE_URL must be set in settings and use the 'postgresql+asyncpg' driver"
    )


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}) -> None:
        # Initialize the async engine with provided host and kwargs
        self._engine: AsyncEngine | None = create_async_engine(host, **engine_kwargs)
        # Initialize the session maker bound to the engine
        self._sessionmaker: async_sessionmaker[AsyncSession] | None = (
            async_sessionmaker(
                autocommit=False,
                bind=self._engine,
                expire_on_commit=False,  # Recommended for FastAPI
            )
        )

    async def close(self) -> None:
        """Close the database engine."""
        if self._engine is None:
            # Should not happen if initialized correctly
            return
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        """Provide a context-managed async database connection."""
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        """Provide a context-managed async database session."""
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
            # Optional: commit here if you want the dependency to handle commits
            # await session.commit()
        except Exception:
            # Rollback on any exception during the session usage
            await session.rollback()
            raise
        finally:
            # Always close the session
            await session.close()


# Global instance of the session manager
# Configure engine kwargs here (e.g., pooling, echo)
sessionmanager = DatabaseSessionManager(
    settings.DATABASE_URL,
    {
        "echo": False,  # Set True for SQL logging
        "pool_size": 10,  # Example pool size
        "max_overflow": 20,  # Example overflow
        "pool_recycle": 1800,  # Example recycle time (30 mins)
    },
)


# FastAPI dependency to get a database session
async def get_db_session() -> AsyncIterator[AsyncSession]:
    async with sessionmanager.session() as session:
        yield session
