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


class ItemUpdateRequest(BaseModel):
    name: str | None = None
    inventary_id: int | None = None
    type: str | None = None
    specification: dict | None = None
    condition: str | None = None
    price: float | None = None
    image: str | None = None
