from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db import BaseSqlModel
from backend.app.models import User


class Token(BaseSqlModel):
    __tablename__ = 'tokens'

    value: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    is_alive: Mapped[bool] = mapped_column(Boolean, default=True)

    user: Mapped['User'] = relationship(back_populates='tokens')
