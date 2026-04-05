import re
from uuid import UUID

from pydantic import EmailStr, Field, field_validator
from typing import Optional, List

from ..schemas import InputSchema, BaseSchema, UserMinimalSchema, RoleMinimalSchema


class UserSchema(UserMinimalSchema):
    roles: List[RoleMinimalSchema] = Field(default_factory=list)


class UserCreateSchema(InputSchema):
    full_name: str = Field(min_length=2, max_length=256)
    email: EmailStr = Field(max_length=256)
    password: str = Field(min_length=8)
    active: Optional[bool] = True
    is_admin: Optional[bool] = False
    role_ids: List[UUID] = Field(default_factory=list)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        errors = []

        if not re.search(r"[A-Z]", value):
            errors.append("missing uppercase letter")

        if not re.search(r"[a-z]", value):
                errors.append("missing lowercase letter")

        if not re.search(r"\d", value):
            errors.append("missing digit")

        if not re.search(r"[^0-9a-zA-Z]", value):
            errors.append("missing special character")

        if errors:
            raise ValueError(", ".join(errors))

        return value


class UserUpdateSchema(BaseSchema):
    full_name: Optional[str] = Field(None, min_length=2, max_length=256)
    email: Optional[EmailStr] = Field(None, max_length=256)
    active: Optional[bool] = None
    is_admin: Optional[bool] = None
    role_ids: Optional[List[UUID]] = None
