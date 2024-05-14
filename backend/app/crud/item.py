from typing import List

from sqlalchemy.orm import Session

from app import models, schemas, errors


def get_item_by_id(db: Session, id: int) -> models.Item:
    item = db.get(models.Item, id)

    return item


# def get_all_items(db: Session) -> List[models.Item]:
#     items = db.query(models.Item).all()
#
#     return items


def create_item(db: Session, item_create: schemas.ItemCreateRequest, is_superuser: bool) -> models.Item:
    if not is_superuser:
        raise errors.PermissionDenied()

    # TODO: add normal specification field from db
    # TODO: add s3 link to image field
    # TODO: handle validation errors

    db_item = models.Item(
        name=item_create.name,
        inventary_id=item_create.inventary_id,
        type=item_create.type,
        specification={},
        condition=item_create.condition,
        price=item_create.price,
        image=item_create.image,
    )

    db.add(db_item)
    db.commit()

    return db_item


def get_all_items_by_filter(db: Session, type: str, search_name: str) -> List[models.Item]:
    query = db.query(models.Item)

    if type:
        query = query.filter(models.Item.type == type)
    if search_name:
        query = query.filter(models.Item.name == search_name)

    items = query.all()

    return items


def update_item(db: Session, item_id: int, item_update: schemas.ItemUpdateRequest) -> models.Item:
    item = db.query(models.Item).filter(models.Item.id == item_id).first()

    if item is None:
        raise errors.ItemNotFoundError()

    for key, value in item_update.dict(exclude_unset=True).items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)

    return item
