from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class InputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BaseSchema(BaseModel):
    model_config = ConfigDict(use_enum_values=True, str_strip_whitespace=True, from_attributes=True)


class PaginationSchema[T](BaseSchema):
    page: int
    size: int
    total_items: int
    total_pages: int
    results: List[T]


class UserMinimalSchema(BaseSchema):
    id: UUID
    full_name: str
    email: str
    active: bool
    is_admin: bool


class RoleMinimalSchema(BaseSchema):
    id: UUID
    name: str


class UserPrincipal(BaseSchema):
    id: UUID
    full_name: str
    email: str
    is_admin: bool
    roles: List[RoleMinimalSchema]
