from pydantic import BaseModel
from datetime import date


class Transaction(BaseModel):
    id: int
    item_id: int
    user_id: int
    type: str
    cost: float
    pledge: float
    start_date: date
    end_date: date
    final_end_date: date | None


class TransactionCreateRequest(BaseModel):
    item_id: int
    pledge: float
    start_date: date
    end_date: date


class TransactionUpdateRequest(BaseModel):
    final_end_date: date
