from typing import List

from sqlalchemy.orm import Session

from app import models, schemas, errors


def create_transaction(db: Session, transaction: schemas.TransactionCreateRequest,
                       item: models.Item, user: models.User) -> models.Transaction:
    db_transaction = models.Transaction(
        item_id=item.id,
        user_id=user.id,
        cost=((transaction.end_date - transaction.start_date).days + 1) * item.price,
        pledge=transaction.pledge,
        start_date=transaction.start_date,
        end_date=transaction.end_date,
        final_end_date=None,
    )

    db.add(db_transaction)
    db.commit()

    return db_transaction
