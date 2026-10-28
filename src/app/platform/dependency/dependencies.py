from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.platform.database.session import get_async_session

# Auth form
OAuth2FormDep = Annotated[OAuth2PasswordRequestForm, Depends()]

# Database session
AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]