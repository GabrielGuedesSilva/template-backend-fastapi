from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr

from .types import NonEmptyStr, UserName


class UserCreateSchema(BaseModel):
    name: UserName
    email: EmailStr
    password: str


class UserSchema(BaseModel):
    id: UUID
    name: UserName
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserUpdateSchema(BaseModel):
    name: Optional[UserName] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
