from src.core.services.user_service import UserService
from src.di.container import container


def get_user_service() -> UserService:
    return container.user_service()
