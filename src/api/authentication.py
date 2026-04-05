from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .exceptions import TokenInvalidException, ForbiddenException, NotAuthenticatedException
from .schemas import UserPrincipal
from src.infrastructure.persistence.tortoise_orm.models import User
from src.config import envSettings


async def authenticated(
        authorization: Annotated[HTTPAuthorizationCredentials | None, Depends(HTTPBearer())],
):
    if authorization is None:
        raise NotAuthenticatedException()
    try:
        payload = jwt.decode(authorization.credentials, envSettings.SECRET_KEY, algorithms=["HS512"])
        user_id: str = payload.get("sub", "")
        user = await User.get_or_none(id=user_id, active=True).prefetch_related("roles")
        if user is None:
            raise TokenInvalidException()
        return UserPrincipal(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
            is_admin=user.is_admin,
            roles=[role for role in user.roles if role.active],
        )
    except jwt.PyJWTError:
        raise TokenInvalidException()

class Authorization:
    def __init__(self, is_admin: bool=False):
        self.is_admin: bool = is_admin

    def __call__(self, user_principal: UserPrincipal = Depends(authenticated)) -> UserPrincipal:
        if self.is_admin and not user_principal.is_admin:
            raise ForbiddenException()
        return user_principal