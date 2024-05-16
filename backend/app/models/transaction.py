from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Float, DateTime, String
from datetime import datetime

from app.db import BaseSqlModel


class Transaction(BaseSqlModel):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    item_id: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer)
    type: Mapped[str] = mapped_column(String)
    cost: Mapped[float] = mapped_column(Float)
    pledge: Mapped[float] = mapped_column(Float)
    start_date: Mapped[datetime] = mapped_column(DateTime)
    end_date: Mapped[datetime] = mapped_column(DateTime)
    final_end_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
