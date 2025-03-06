from typing import Annotated

from fastapi import Depends

from src.core.services.user_service import UserService
from src.di.providers import get_user_service

UserServiceDependency = Annotated[UserService, Depends(get_user_service)]
