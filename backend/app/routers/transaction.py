from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, crud, errors, serializers, models
from app.dependencies import get_db, current_user

transaction_router = APIRouter(
    prefix="/transaction",
    tags=["Transaction"],
)


@transaction_router.post(path="/create")
def create_transaction(transaction: schemas.TransactionCreateRequest = Body(...),
                       db: Session = Depends(get_db),
                       user: models.User = Depends(current_user)) -> schemas.Transaction:
    db_item = crud.get_item_by_id(db, transaction.item_id)
    db_transaction = crud.create_transaction(db, transaction, db_item, user)

    return serializers.get_transaction(db_transaction)