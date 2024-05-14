from typing import List

from app import schemas
from app.models import transaction as db_model_transaction


def get_transaction(db_transaction: db_model_transaction.Transaction) -> schemas.Transaction:
    transaction = schemas.Transaction(
        id=db_transaction.id,
        item_id=db_transaction.item_id,
        user_id=db_transaction.user_id,
        cost=db_transaction.cost,
        pledge=db_transaction.pledge,
        start_date=db_transaction.start_date,
        end_date=db_transaction.end_date,
        final_end_date=db_transaction.final_end_date,
    )

    return transaction


def get_transactions(db_transactions: List[db_model_transaction.Transaction]) -> List[schemas.Transaction]:
    transactions = [get_transaction(db_transaction) for db_transaction in db_transactions]
    return transactions
