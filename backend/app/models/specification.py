from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, JSON

from app.db import BaseSqlModel


class Specification(BaseSqlModel):
    __tablename__ = "specifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    item_type: Mapped[str] = mapped_column(String)
    config: Mapped[dict] = mapped_column(JSON)
