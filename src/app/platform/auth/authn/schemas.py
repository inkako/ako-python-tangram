from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class UserCreateSchema(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=100)]
    email: Annotated[EmailStr, Field(min_length=1, max_length=100)]
    phone: Annotated[str, Field(min_length=1, max_length=15)]
    username: Annotated[str, Field(min_length=1, max_length=30)]
    password: Annotated[str, Field(min_length=8, max_length=100)]


class UserUpdateSchema(BaseModel):
    ...
