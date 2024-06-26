from typing import List

from app.models import user as db_model_user
from app import schemas


def get_user(db_user: db_model_user.User) -> schemas.User:
    user = schemas.User(
        id=db_user.id,
        email=db_user.email,
        name=db_user.name,
        is_superuser=db_user.is_superuser,
    )

    return user


def get_users(db_users: List[db_model_user.User]) -> List[schemas.User]:
    users = [get_user(db_user) for db_user in db_users]

    return users
