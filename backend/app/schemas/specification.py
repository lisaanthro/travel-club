from pydantic import BaseModel


class Specification(BaseModel):
    id: int
    item_type: str
    config: dict
