from sqlalchemy.orm import Session
from app import models, errors, utils


def create_token(db: Session, user_id: int) -> models.Token:
    """Создание токена"""
    db_token = models.Token(
        value=utils.generate_bearer_token(10),
        user_id=user_id,
        is_alive=True,
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)

    return db_token


def read_token(db: Session, value: str) -> models.Token:
    """Получение токена"""
    token = db.query(models.Token).filter(models.Token.value == value).first()

    if token is None:
        raise errors.AuthenticationError()

    return token