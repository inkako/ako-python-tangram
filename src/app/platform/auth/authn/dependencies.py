from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

# Auth form
OAuth2FormDep = Annotated[OAuth2PasswordRequestForm, Depends()]
