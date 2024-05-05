from sqlalchemy.orm import Session

from backend.app.models import user


def get_all_users(db: Session):
    db_users = db.query(user.User).all()

    return db_users
