from typing import List

from sqlalchemy.orm import Session

from app.crud import get_item_by_id
from app import models, schemas, errors


def create_transaction(
    db: Session,
    transaction: schemas.TransactionCreateRequest,
    item: models.Item,
    user: models.User,
    transaction_type: str,
) -> models.Transaction:
    if transaction_type not in ["rent", "repair"]:
        raise errors.TransactionTypeError()

    transaction = models.Transaction(
        item_id=item.id,
        user_id=user.id,
        type=transaction_type,
        cost=((transaction.end_date - transaction.start_date).days + 1) * item.price,
        pledge=transaction.pledge,
        start_date=transaction.start_date,
        end_date=transaction.end_date,
        final_end_date=None,
    )

    db.add(transaction)
    db.commit()

    return transaction


def get_transaction_by_id(db: Session, transaction_id: int) -> models.Transaction:
    transaction = (
        db.query(models.Transaction)
        .filter(models.Transaction.id == transaction_id)
        .first()
    )

    return transaction


def get_all_transactions(db: Session) -> List[models.Transaction]:
    transactions = db.query(models.Transaction).all()

    return transactions


def update_transaction(
    db: Session,
    transaction_id: int,
    transaction_update: schemas.TransactionUpdateRequest,
) -> models.Transaction:
    transaction = (
        db.query(models.Transaction)
        .filter(models.Transaction.id == transaction_id)
        .first()
    )

    if transaction is None:
        raise errors.TransactionNonFound

    item = get_item_by_id(db, transaction.item_id)
    transaction.cost = (
        (transaction_update.final_end_date - transaction.start_date).days + 1
    ) * item.price

    for key, value in transaction_update.dict(exclude_unset=True).items():
        setattr(transaction, key, value)

    db.commit()
    db.refresh(transaction)

    return transaction


def get_transactions_by_user_id(db: Session, user_id: int) -> List[models.Transaction]:
    transactions = (
        db.query(models.Transaction).filter(models.Transaction.user_id == user_id).all()
    )

    return transactions


def get_transactions_by_item_id(db: Session, item_id: int) -> List[models.Transaction]:
    transactions = (
        db.query(models.Transaction).filter(models.Transaction.item_id == item_id).all()
    )

    return transactions
