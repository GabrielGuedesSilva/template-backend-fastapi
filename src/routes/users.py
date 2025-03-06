from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Request

from src.core.schemas.user_schemas import UserPublic, UserSchema, UserUpdate
from src.database.query.query import Query
from src.di.dependencies import UserServiceDependency

router = APIRouter(
    prefix='/users',
    tags=['users'],
)


@router.post('', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(
    request: Request,
    user: UserSchema,
    user_service: UserServiceDependency,
):
    result = user_service.add(user)
    return result


@router.get('', status_code=HTTPStatus.OK, response_model=List[UserPublic])
def get_users(
    request: Request,
    user_service: UserServiceDependency,
):
    query = Query(request.query_params)
    users = user_service.get_all(query)
    return users


@router.get('/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def get_user_by_id(
    request: Request,
    user_id: int,
    user_service: UserServiceDependency,
):
    user = user_service.get_by_id(user_id)
    return user


@router.patch(
    '/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(
    request: Request,
    user_id: int,
    user: UserUpdate,
    user_service: UserServiceDependency,
):
    updated_user = user_service.update(user_id, user)
    return updated_user


@router.delete('/{user_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_user(
    request: Request,
    user_id: int,
    user_service: UserServiceDependency,
):
    user_service.remove(user_id)
