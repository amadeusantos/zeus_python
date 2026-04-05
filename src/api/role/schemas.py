from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from ..schemas import InputSchema, RoleMinimalSchema


class RoleSchema(RoleMinimalSchema):
    description: str
    active: bool


class RoleCreateSchema(InputSchema):
    name: str = Field(min_length=2, max_length=128)
    description: str
    active: Optional[bool] = True


class RoleUpdateSchema(BaseModel):
    name: Optional[str] = Field(None,min_length=2, max_length=128)
    description: Optional[str] = None
    active: Optional[bool] = None
