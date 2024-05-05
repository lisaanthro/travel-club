from backend.app.db import SessionLocal


def get_db():
    with SessionLocal() as db:
        yield db