from pydantic import BaseModel
from .user import User


class Token(BaseModel):
    bearer_token: str
    user: User
