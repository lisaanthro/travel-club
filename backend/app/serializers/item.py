from typing import List

from app import schemas
from app.models import item as db_model_item


def get_item(db_item: db_model_item.Item) -> schemas.Item:
    item = schemas.Item(
        id=db_item.id,
        name=db_item.name,
        inventary_id=db_item.inventary_id,
        type=db_item.type,
        specification=db_item.specification,
        condition=db_item.condition,
        price=db_item.price,
        image=db_item.image,
    )

    return item


def get_items(db_items: List[db_model_item.Item]) -> List[schemas.Item]:
    items = [get_item(db_item) for db_item in db_items]

    return items
