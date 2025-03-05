from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel

from src.database.query.query import Query
from src.database.repositories.base_repository import BaseRepository

# Definindo os tipos genéricos
ModelType = TypeVar('ModelType')
SchemaType = TypeVar('SchemaType', bound=BaseModel)


class BaseService(Generic[ModelType, SchemaType]):
    def __init__(
        self,
        repository: BaseRepository[ModelType, SchemaType],
        unique_fields: List[str],
    ):
        self.repository = repository
        self.unique_fields = unique_fields

    def add(self, schema: SchemaType) -> ModelType:
        self.repository.check_duplicity(schema, self.unique_fields)
        return self.repository.create(schema)

    def get_all(self, query: Query) -> List[ModelType]:
        return self.repository.find(query)

    def get_by_id(self, id: int) -> Optional[ModelType]:
        self.repository.check_exists(id)
        return self.repository.find_by_id(id)

    def update(self, id: int, schema: SchemaType) -> Optional[ModelType]:
        self.repository.check_exists(id)
        return self.repository.update(id, schema)

    def remove(self, id: int) -> bool:
        self.repository.check_exists(id)
        return self.repository.delete(id)
