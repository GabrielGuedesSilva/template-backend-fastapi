from http import HTTPStatus
from typing import Generic, List, TypeVar, Union
from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel

from src.database.query import Query
from src.database.repositories.base_repository import BaseRepository
from src.utils.exceptions_messages import ExceptionsMessages

# Definindo os tipos genéricos
ModelType = TypeVar('ModelType')
SchemaType = TypeVar('SchemaType', bound=BaseModel)


class BaseService(Generic[ModelType]):
    def __init__(
        self,
        repository: BaseRepository[ModelType],
        unique_fields: List[str],
    ):
        self.repository = repository
        self.unique_fields = unique_fields

    def add(self, schema: SchemaType) -> ModelType:
        self.repository.check_duplicity(schema, self.unique_fields)
        return self.repository.create(schema)

    def get_all(self, query: Query) -> List[ModelType]:
        return self.repository.find(query)

    def get_one(self, query: Query) -> Union[ModelType, None]:
        result = self.repository.find_one(query)
        if result is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=ExceptionsMessages.NOT_FOUND.format(
                    model=self.repository.model_name,
                ),
            )
        return result

    def get_by_id(self, id: UUID) -> Union[ModelType, None]:
        self.repository.check_exists(id)
        return self.repository.find_by_id(id)

    def update(self, id: UUID, schema: SchemaType) -> ModelType:
        self.repository.check_exists(id)
        return self.repository.update(id, schema)

    def remove(self, id: UUID) -> bool:
        self.repository.check_exists(id)
        return self.repository.delete(id)
