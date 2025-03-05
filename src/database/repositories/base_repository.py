from http import HTTPStatus
from typing import Generic, List, Type, TypeVar

from fastapi import HTTPException
from loguru import logger
from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.database.query.query import Query
from src.utils.exceptions_messages import ExceptionsMessages

ModelType = TypeVar('ModelType')
SchemaType = TypeVar('SchemaType')


class BaseRepository(Generic[ModelType, SchemaType]):
    def __init__(self, db_connection: Session, model: Type[ModelType]):
        self.db_connection = db_connection
        self.model = model
        self.model_name = self.model.__name__

    def create(self, schema: SchemaType):
        db_model = self.model(**schema.dict())
        self.db_connection.session.add(db_model)
        self.db_connection.session.commit()
        self.db_connection.session.refresh(db_model)
        return db_model

    def find(self, query: Query) -> List[ModelType]:
        query_builder = self.db_connection.session.query(self.model).order_by(
            self.model.id
        )

        for key, value in query.filters.items():
            if hasattr(self.model, key):
                query_builder = query_builder.filter(
                    getattr(self.model, key) == value
                )

        if query.limit is not None:
            query_builder = query_builder.limit(query.limit)

        query_builder = query_builder.offset(query.offset)

        return query_builder.all()

    def find_by_id(self, id: int) -> ModelType:
        query_builder = self.db_connection.session.query(self.model).filter_by(
            id=id
        )

        return query_builder.first()

    def update(self, id: int, schema: SchemaType) -> ModelType:
        db_model = self.find_by_id(id)

        for key, value in schema.dict(exclude_unset=True).items():
            setattr(db_model, key, value)

        self.db_connection.session.commit()
        self.db_connection.session.refresh(db_model)

        return db_model

    def delete(self, id: int) -> bool:
        db_model = self.find_by_id(id)

        self.db_connection.session.delete(db_model)
        self.db_connection.session.commit()

        return True

    def check_exists(self, id: int):
        if self.find_by_id(id) is not None:
            return True
        else:
            logger.error(
                ExceptionsMessages.ID_NOT_FOUND.format(model=self.model_name)
            )
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=ExceptionsMessages.ID_NOT_FOUND.format(
                    model=self.model_name
                ),
            )

    def check_duplicity(self, schema: SchemaType, unique_fields):
        filters = [
            getattr(self.model, field) == getattr(schema, field)
            for field in unique_fields
            if hasattr(schema, field)
        ]

        if not filters:
            return False

        existing_record = (
            self.db_connection.session.query(self.model)
            .filter(or_(*filters))
            .first()
        )

        if existing_record:
            conflict_fields = [
                f"{field}='{getattr(schema, field)}'"
                for field in unique_fields
                if hasattr(schema, field)
                and getattr(existing_record, field) == getattr(schema, field)
            ]
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=ExceptionsMessages.already_exists(
                    self.model_name, conflict_fields
                ),
            )
