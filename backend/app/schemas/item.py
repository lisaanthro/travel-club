from pydantic import BaseModel


class Item(BaseModel):
    id: int
    name: str
    inventary_id: int
    type: str
    specification: dict
    condition: str
    price: float
    image: str


class ItemCreateRequest(BaseModel):
    name: str
    inventary_id: int
    type: str
    # specification: dict
    condition: str
    price: float
    image: str
