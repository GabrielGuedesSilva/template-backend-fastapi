from sqlalchemy.orm import Session

from src.core.schemas.user_schemas import UserSchema
from src.database.models.user import User
from src.database.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User, UserSchema]):
    def __init__(self, db_connection: Session):
        super().__init__(db_connection, User)
