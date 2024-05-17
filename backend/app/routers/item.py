from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, crud, errors, serializers, models
from app.dependencies import get_db, current_user

item_router = APIRouter(
    prefix="/item",
    tags=["Item"],
)


@item_router.get(path="/{item_id}")
def get_item_by_id(item_id: int, db: Session = Depends(get_db)) -> schemas.Item:
    db_item = crud.get_item_by_id(db, item_id)

    return serializers.get_item(db_item)


@item_router.get(path="")
def get_all_items(type: str | None = None,
                  search_name: str | None = None,
                  db: Session = Depends(get_db)) -> List[schemas.Item]:
    db_items = crud.get_all_items_by_filter(db,
                                            type=type,
                                            search_name=search_name)

    return serializers.get_items(db_items)


@item_router.post(path="/create")
def create_item(item: schemas.ItemCreateRequest,
                db: Session = Depends(get_db),
                user: models.User = Depends(current_user)) -> schemas.Item:
    db_item = crud.create_item(db, item, user.is_superuser)

    return serializers.get_item(db_item)

# @item_router.get(path="/list/{type}")
# def get_all_items_by_type(type: str, db: Session = Depends(get_db)) -> List[schemas.Item]:
#     db_items = crud.get_all_items_by_type(db, type)
#
#     return serializers.get_items(db_items)


@item_router.put(path="/{item_id}")
def update_item(item_id: int,
                item_update: schemas.ItemUpdateRequest = Body(...),
                db: Session = Depends(get_db)) -> schemas.Item:
    db_item = crud.update_item(db, item_id, item_update)

    return serializers.get_item(db_item)
