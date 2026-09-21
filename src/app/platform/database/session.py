from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.platform.config.settings import get_settings

settings = get_settings()

_async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.POSTGRES_ECHO if settings.POSTGRES_ECHO else False,
    pool_size=settings.POSTGRES_POOL_SIZE if settings.POSTGRES_POOL_SIZE else 20,
    max_overflow=settings.POSTGRES_MAX_OVERFLOW if settings.POSTGRES_MAX_OVERFLOW else 2,
)

_async_session = async_sessionmaker[AsyncSession](
    _async_engine,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with _async_session() as session:
        yield session