from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.services.user_service import UserService
from src.database.repositories.user_repository import UserRepository


class Container(containers.DeclarativeContainer):
    # Config
    config = providers.Configuration()

    # Engine
    engine = providers.Singleton(create_engine, config.DATABASE_URL)

    # Session
    session = providers.Factory(sessionmaker, bind=engine)

    # Repositories
    user_repository = providers.Factory(UserRepository, session=session)

    # Services
    user_service = providers.Factory(
        UserService, user_repository=user_repository
    )
