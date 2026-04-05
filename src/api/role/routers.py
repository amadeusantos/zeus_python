from typing import Annotated, Optional, Any
from uuid import UUID

from fastapi import APIRouter, Query, Depends
from starlette import status

from src.infrastructure.persistence.tortoise_orm.models import Role
from .exceptions import RoleNotFoundException
from .schemas import RoleSchema, RoleCreateSchema, RoleUpdateSchema
from .validations import validate_name
from ..authentication import Authorization
from ..database import pagination
from ..schemas import PaginationSchema, UserPrincipal

router = APIRouter(prefix="/roles", tags=["roles"])

async def get_role_by_id(id: UUID) -> Role:
    role = await Role.get_or_none(id=id)
    if not role:
        raise RoleNotFoundException()
    return role

@router.post("", response_model=RoleSchema, status_code=status.HTTP_201_CREATED)
async def create_role(role_data: RoleCreateSchema, _: UserPrincipal = Depends(Authorization(is_admin=True))):
    await validate_name(role_data.name)

    role = await Role.create(**role_data.model_dump())
    return role

@router.get("", response_model=PaginationSchema[RoleSchema])
async def get_roles(
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1)] = 10,
    ordering: Annotated[
        Optional[str], Query()
    ] = None,
    name: Annotated[Optional[str], Query()] = None,
    active: Annotated[Optional[bool], Query()] = None,
    _: UserPrincipal = Depends(Authorization(is_admin=True)),
):
    filters: dict[str, Any] = {}

    if name:
        filters.setdefault("name", name)

    if active is not None:
        filters.setdefault("active", active)

    orderings = []
    if ordering:
        orderings.append(ordering)
    return await pagination(Role, page, size, orderings, filters)


@router.get("/{id}", response_model=RoleSchema)
async def get_role(id: UUID, _: UserPrincipal = Depends(Authorization(is_admin=True))):
    return await get_role_by_id(id)


@router.patch("/{id}", response_model=RoleSchema)
async def update_role(id: UUID, role_data: RoleUpdateSchema, _: UserPrincipal = Depends(Authorization(is_admin=True))):
    role = await get_role_by_id(id)

    if role_data.name and role.name != role_data.name:
        await validate_name(role_data.name)

    await role.update_from_dict(role_data.model_dump(exclude_unset=True))
    await role.save()
    return role


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(id: UUID, _: UserPrincipal = Depends(Authorization(is_admin=True))):
    role = await get_role_by_id(id)
    await role.delete()
    return None
