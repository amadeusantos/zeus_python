from src.infrastructure.persistence.tortoise_orm.models import Role
from .exceptions import RoleNameAlreadyExistsException


async def validate_name(name: str):
    if await Role.filter(name=name).exists():
        raise RoleNameAlreadyExistsException()