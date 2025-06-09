from src.core.schemas.user_schemas import UserCreateSchema
from test.mocks.user import UserFactory


def test_create_user_by_service(user_service):
    data = UserFactory.build()
    new_user = UserCreateSchema(**data)

    user = user_service.add(new_user)

    assert user.id is not None
    assert user.name == data['name']
    assert user.email == data['email']
    assert user.password == data['password']
