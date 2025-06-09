from http import HTTPStatus
from typing import Generic, List, Type, TypeVar, Union
from uuid import UUID

from fastapi import HTTPException
from loguru import logger
from pydantic import BaseModel
from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.database.query import Query
from src.utils.exceptions_messages import ExceptionsMessages

ModelType = TypeVar('ModelType')
SchemaType = TypeVar('SchemaType', bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    def __init__(self, session: Session, model: Type[ModelType]):
        self.session = session()
        self.model = model
        self.model_name = self.model.__name__

    def create(self, schema: SchemaType) -> ModelType:
        db_model = self.model(**schema.model_dump())
        self.session.add(db_model)
        self.session.commit()
        self.session.refresh(db_model)
        return db_model

    def find(self, query: Query) -> List[ModelType]:
        query_builder = self.session.query(self.model).order_by(
            self.model.created_at.desc()
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

    def find_by_id(self, id: UUID) -> ModelType:
        query_builder = self.session.query(self.model).filter_by(id=id)
        return query_builder.first()

    def find_one(self, query: Query) -> Union[ModelType, None]:
        query_builder = self.session.query(self.model)

        for key, value in query.filters.items():
            if hasattr(self.model, key):
                query_builder = query_builder.filter(
                    getattr(self.model, key) == value
                )

        return query_builder.first()

    def update(self, id: UUID, schema: SchemaType) -> ModelType:
        db_model = self.find_by_id(id)

        for key, value in schema.model_dump(exclude_unset=True).items():
            setattr(db_model, key, value)

        self.session.commit()
        self.session.refresh(db_model)

        return db_model

    def delete(self, id: UUID) -> bool:
        db_model = self.find_by_id(id)

        self.session.delete(db_model)
        self.session.commit()

        return True

    def check_exists(self, id: UUID) -> bool:
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

    def check_duplicity(
        self, schema: SchemaType, unique_fields: List[str]
    ) -> bool:
        filters = [
            getattr(self.model, field) == getattr(schema, field)
            for field in unique_fields
            if hasattr(schema, field)
        ]

        if not filters:
            return False

        existing_record = (
            self.session.query(self.model).filter(or_(*filters)).first()
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
