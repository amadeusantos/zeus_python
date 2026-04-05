from datetime import datetime, timezone, timedelta

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError, InvalidHashError
from fastapi import APIRouter, Depends
from src.config import envSettings

from .exceptions import InvalidCredentialsException, UserInactiveException
from src.infrastructure.persistence.tortoise_orm.models import User
from .schemas import AuthenticateSchema, TokenSchema
from ..authentication import authenticated
from ..schemas import UserPrincipal

router = APIRouter(prefix="/auth", tags=["auth"])

async def get_user_by_email(email: str) -> User:
    user = await User.get_or_none(email=email)
    if not user:
        raise InvalidCredentialsException()

    if not user.active:
        raise UserInactiveException()
    return user

@router.post("/authenticate", response_model=TokenSchema)
async def authenticate(data: AuthenticateSchema):
    user = await get_user_by_email(data.email)
    password_hasher = PasswordHasher()
    try:
        password_hasher.verify(user.password, data.password)
    except (VerificationError, VerifyMismatchError, InvalidHashError):
        raise InvalidCredentialsException()
    token = jwt.encode({"sub": str(user.id), 'iat': datetime.now(timezone.utc),
                        'exp': datetime.now(timezone.utc) + timedelta(days=1)}, envSettings.SECRET_KEY,
                       algorithm="HS512")
    return TokenSchema(access_token=token, token_type="bearer", expires_in=int(timedelta(days=1).total_seconds()))

@router.get("/authenticated", response_model=UserPrincipal)
async def authenticated_user(user_principal: UserPrincipal = Depends(authenticated)):
    return user_principal