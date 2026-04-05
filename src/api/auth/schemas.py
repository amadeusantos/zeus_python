from pydantic import EmailStr

from ..schemas import BaseSchema, InputSchema


class AuthenticateSchema(InputSchema):
    email: EmailStr
    password: str

class TokenSchema(BaseSchema):
    expires_in: int
    token_type: str
    access_token: str