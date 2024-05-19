from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import schemas, crud, errors, serializers, models
from app.dependencies import get_db, current_user

transaction_router = APIRouter(
    prefix="/transaction",
    tags=["Transaction"],
)


@transaction_router.post(path="/create/{transaction_type:str}")
def create_rent_transaction(transaction_type, transaction: schemas.TransactionCreateRequest = Body(...),
                            db: Session = Depends(get_db),
                            user: models.User = Depends(current_user)) -> schemas.Transaction:
    try:
        db_item = crud.get_item_by_id(db, transaction.item_id)
        db_transaction = crud.create_transaction(db, transaction, db_item, user, transaction_type)

        return serializers.get_transaction(db_transaction)

    except errors.TransactionTypeError as e:
        raise HTTPException(status_code=401, detail=str(e))


@transaction_router.get(path="/{transaction_id:int}")
def get_transaction_by_id(transaction_id: int, db: Session = Depends(get_db),
                          user: models.User = Depends(current_user)) -> schemas.Transaction:
    db_transaction = crud.get_transaction_by_id(db, transaction_id)

    return serializers.get_transaction(db_transaction)


@transaction_router.get(path="/")
def get_all_transactions(db: Session = Depends(get_db),
                         user: models.User = Depends(current_user)) -> List[schemas.Transaction]:
    db_transactions = crud.get_all_transactions(db)

    return serializers.get_transactions(db_transactions)


@transaction_router.put(path="/{transaction_id:int}")
def update_transaction(transaction_id: int,
                       transaction_update: schemas.TransactionUpdateRequest = Body(...),
                       db: Session = Depends(get_db),
                       user: models.User = Depends(current_user)) -> schemas.Transaction:
    db_transaction = crud.update_transaction(db, transaction_id, transaction_update)

    return serializers.get_transaction(db_transaction)


@transaction_router.get(path="/user/{user_id:int}")
def get_transactions_by_user_id(user_id: int,
                                db: Session = Depends(get_db)) -> List[schemas.Transaction]:
    db_transactions = crud.get_transactions_by_user_id(db, user_id)

    return serializers.get_transactions(db_transactions)


@transaction_router.get(path="/item/{item_id:int}")
def get_transactions_by_item_id(item_id: int,
                                db: Session = Depends(get_db)) -> List[schemas.Transaction]:
    db_transactions = crud.get_transactions_by_item_id(db, item_id)

    return serializers.get_transactions(db_transactions)


@transaction_router.get(path="/user/profile")
def get_transactions_of_current_user(db: Session = Depends(get_db),
                                     user: models.User = Depends(current_user)) -> List[schemas.Transaction]:
    db_transactions = crud.get_transactions_by_user_id(db, user.id)

    return serializers.get_transactions(db_transactions)
