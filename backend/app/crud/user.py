from sqlalchemy.orm import Session

from app import models, schemas, errors
from .token import read_token


def get_all_users(db: Session):
    """Получение всех пользователей"""
    db_users = db.query(models.User).all()

    return db_users


def create_user(db: Session, payload: schemas.UserCreateRequest) -> models.User:
    """Создание пользователя"""

    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if user is not None:
        raise errors.EmailAlreadyAssociatedError()

    db_user = models.User(
        email=payload.email,
        name=payload.name,
        is_superuser=True,
    )
    db_user.set_password(payload.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def read_user_by_login(db: Session, payload: schemas.UserLoginRequest) -> models.User:
    """Получение пользователя"""
    user = db.query(models.User).filter(models.User.email == payload.email).first()

    if user is None:
        raise errors.AuthenticationError()

    if user.check_password(password=payload.password):
        return user

    raise errors.AuthenticationError()


def read_user_by_token(db: Session, token: str) -> models.User:
    """Получение пользователя по токену"""
    token = read_token(db, token)

    user = db.query(models.User).filter(models.User.id == token.user_id).first()

    if user is None:
        raise errors.UserNotFoundError()

    return user


def update_user(
    db: Session, user_id: int, user_update: schemas.UserUpdateRequest
) -> models.User:
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        raise errors.UserNotFoundError()

    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user
