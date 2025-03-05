from http import HTTPStatus

from fastapi import HTTPException

from src.core.schemas.user_schemas import UserSchema
from src.core.services.base_service import BaseService
from src.database.models.user import User
from src.database.repositories.user_repository import UserRepository
from src.utils.constant_values import ConstantValues
from src.utils.exceptions_messages import ExceptionsMessages


class UserService(BaseService[User, UserSchema]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(user_repository, unique_fields=['username', 'email'])

    def add(self, schema: UserSchema) -> User:
        if len(schema.username) < ConstantValues.USERNAME_SIZE:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=ExceptionsMessages.INVALID_USERNAME_SIZE,
            )

        return super().add(schema)
