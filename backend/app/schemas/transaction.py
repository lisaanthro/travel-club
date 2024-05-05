from pydantic import BaseModel
from datetime import datetime


class Transaction(BaseModel):
    id: int
    item_id: int
    user_id: int
    cost: float
    pledge: float
    start_date: datetime
    end_date: datetime
    final_end_date: datetime
