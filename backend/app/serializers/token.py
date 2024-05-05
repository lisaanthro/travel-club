from backend.app.models import token as db_model_token
from backend.app import schemas
from .user import get_user


def get_token(db_token: db_model_token.Token) -> schemas.Token:
    token = schemas.Token(
        bearer_token=db_token.value,
        user=get_user(db_token.user),
    )

    return token
