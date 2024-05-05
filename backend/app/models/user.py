from backend.app.db import BaseSqlModel

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class User(BaseSqlModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    role: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, nullable=False)
