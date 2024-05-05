from backend.app.db import BaseSqlModel

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Float, DateTime
from datetime import datetime


class Transaction(BaseSqlModel):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    item_id: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer)
    cost: Mapped[float] = mapped_column(Float)
    pledge: Mapped[float] = mapped_column(Float)
    start_date: Mapped[datetime] = mapped_column(DateTime)
    end_date: Mapped[datetime] = mapped_column(DateTime)
    final_end_date: Mapped[datetime] = mapped_column(DateTime)