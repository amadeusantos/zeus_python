from uuid import UUID
from typing import List
from src.infrastructure.persistence.tortoise_orm.models import User, Role

async def sync_roles(user: User, role_ids: List[UUID]):
    roles = await Role.filter(id__in=role_ids)
    await user.roles.clear()
    if roles:
        await user.roles.add(*roles)
