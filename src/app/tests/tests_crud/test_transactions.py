from sqlalchemy.orm import Session

from app.crud.crud_transaction import crud_transaction
from app.schemas.schema_transaction import SchemaTransaction, SchemaTransactionCreate
from app.tests.utils import generate_random_amount, generate_random_date

from .test_accounts import create_random_account


def create_random_transaction(db: Session) -> SchemaTransaction:
    account_id = create_random_account(db=db).id
    transaction_date = generate_random_date()
    amount = generate_random_amount()

    transaction_in = SchemaTransactionCreate(account_id=account_id, transaction_date=transaction_date, amount=amount)
    transaction = crud_transaction.create(db=db, obj_in=transaction_in)
    return transaction


def test_create_transaction(db: Session) -> None:
    transaction = create_random_transaction(db=db)
    assert transaction.id
    assert transaction.amount


def test_get_transaction_by_number(db: Session):
    transaction = create_random_transaction(db=db)
    transactions_by_number = crud_transaction.get_multi_by_account_number(
        db, account_number=transaction.account.account_number
    )
    assert type(transactions_by_number) == list
    assert len(transactions_by_number) > 0
    assert transactions_by_number[0].account.account_number == transaction.account.account_number
