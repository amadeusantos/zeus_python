from fastapi import APIRouter, status, Query, Depends
from argon2 import PasswordHasher
from typing import Optional, Any, Annotated
from uuid import UUID

from src.config import envSettings
from src.infrastructure.persistence.tortoise_orm.models import User
from .exceptions import UserNotFoundException
from .validations import validate_email
from .schemas import UserCreateSchema, UserUpdateSchema, UserSchema
from .actions import sync_roles
from ..authentication import Authorization
from ..database import pagination
from ..schemas import PaginationSchema, UserMinimalSchema, UserPrincipal

router = APIRouter(prefix="/users", tags=["users"])


async def get_user_by_id(id: UUID) -> User:
    user = await User.get_or_none(id=id).prefetch_related("roles")
    if not user:
        raise UserNotFoundException()
    return user


@router.post("", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreateSchema, _: UserPrincipal = Depends(Authorization(is_admin=True))):

    await validate_email(user_data.email)

    user_create = user_data.model_dump(exclude={"role_ids"})
    password_hasher = PasswordHasher(salt_len=envSettings.ARGON2_SALT_LENGTH)
    user_create["password"] = password_hasher.hash(user_create["password"])

    user = await User.create(**user_create)
    await sync_roles(user, user_data.role_ids)
    return await get_user_by_id(user.id)


@router.get("", response_model=PaginationSchema[UserMinimalSchema])
async def get_users(
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1)] = 10,
    ordering: Annotated[
        Optional[str], Query()
    ] = None,
    email: Annotated[Optional[str], Query()] = None,
    active: Annotated[Optional[bool], Query()] = None,
    full_name_contains: Annotated[Optional[str], Query()] = None,
    _: UserPrincipal = Depends(Authorization(is_admin=True)),
):
    filters: dict[str, Any] = {}

    if email:
        filters.setdefault("email", email)

    if active is not None:
        filters.setdefault("active", active)

    if full_name_contains:
        filters.setdefault("full_name__icontains", full_name_contains)

    orderings = []
    if ordering:
        orderings.append(ordering)
    return await pagination(User, page, size, orderings, filters)


@router.get("/{id}", response_model=UserSchema)
async def get_user(id: UUID, _: UserPrincipal = Depends(Authorization(is_admin=True))):
    return await get_user_by_id(id)


@router.patch("/{id}", response_model=UserSchema)
async def update_user(id: UUID, user_data: UserUpdateSchema, _: UserPrincipal = Depends(Authorization(is_admin=True))):
    user = await get_user_by_id(id)

    if user_data.email and user.email != user_data.email:
        await validate_email(user_data.email)

    if user_data.role_ids is not None:
        await sync_roles(user, user_data.role_ids)

    await user.update_from_dict(user_data.model_dump(exclude_unset=True, exclude={"role_ids"}))
    await user.save()
    return await get_user_by_id(user.id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: UUID, _: UserPrincipal = Depends(Authorization(is_admin=True))):
    user = await get_user_by_id(id)
    await user.delete()
    return None
