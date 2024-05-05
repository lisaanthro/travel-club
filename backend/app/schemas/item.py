from pydantic import BaseModel


class Item(BaseModel):
    id: int
    inventary_id: str | int
    type: str
    specification: dict
    condition: str
    price: float
    image: str
