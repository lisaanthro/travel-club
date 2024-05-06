from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, JSON, Float

from app.db import BaseSqlModel


class Item(BaseSqlModel):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    inventary_id: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[str] = mapped_column(String)
    specification: Mapped[dict] = mapped_column(JSON)
    condition: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)
    image: Mapped[str] = mapped_column(String)
