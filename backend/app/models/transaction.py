from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Float, Date, String, ForeignKey
from datetime import date

from app.db import BaseSqlModel


class Transaction(BaseSqlModel):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    item_id: Mapped[int] = mapped_column(Integer, ForeignKey("items.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    type: Mapped[str] = mapped_column(String)
    cost: Mapped[float] = mapped_column(Float)
    pledge: Mapped[float] = mapped_column(Float)
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    final_end_date: Mapped[date] = mapped_column(Date, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="transactions")
    item: Mapped["Item"] = relationship("Item", back_populates="transactions")
