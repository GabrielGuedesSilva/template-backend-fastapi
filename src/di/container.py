from dependency_injector import containers, providers

from src.core.services.user_service import UserService
from src.database.database_connection import DatabaseConnection
from src.database.repositories.user_repository import UserRepository
from src.utils.settings import Settings


class Container(containers.DeclarativeContainer):
    # Config
    settings = providers.Singleton(Settings)

    # Database
    db_connection = providers.Singleton(
        DatabaseConnection,
        database_url=settings.provided.DATABASE_URL,
    )

    # Repositories
    user_repository = providers.Singleton(
        UserRepository, db_connection=db_connection
    )

    # Services
    user_service = providers.Factory(
        UserService, user_repository=user_repository
    )


container = Container()
