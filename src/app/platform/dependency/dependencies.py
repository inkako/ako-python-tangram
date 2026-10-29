from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.platform.database.session import get_async_session

# Database session
AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
