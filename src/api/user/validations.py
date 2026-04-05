from .exceptions import UserEmailAlreadyExistsException
from src.infrastructure.persistence.tortoise_orm.models import User


async def validate_email(email: str):
    if await User.filter(email=email).exists():
        raise UserEmailAlreadyExistsException()
