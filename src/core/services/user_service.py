from http import HTTPStatus

from fastapi import HTTPException

from src.core.schemas.user_schemas import UserCreateSchema
from src.core.services.base_service import BaseService
from src.database.models.user import User
from src.database.repositories.user_repository import UserRepository
from src.utils.constant_values import ConstantValues
from src.utils.exceptions_messages import ExceptionsMessages


class UserService(BaseService[User]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(user_repository, unique_fields=['email'])

    def add(self, schema: UserCreateSchema) -> User:
        return super().add(schema)
