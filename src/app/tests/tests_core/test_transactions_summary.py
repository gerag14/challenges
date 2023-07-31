from decimal import Decimal

from sqlalchemy.orm import Session

from app.core.transactions_summary import TransactionsSummary
from app.tests.tests_crud.test_transactions import create_random_transaction
from app.utils import get_month_name


def tests_load_data_from_csv(db: Session):
    txn = create_random_transaction(db=db)

    data_summary = TransactionsSummary(db=db).create_summary()
    assert data_summary
    assert data_summary.months_summary

    for month_account in data_summary.months_summary:
        if month_account.account_id == txn.account_id:
            summary = month_account
            break

    assert summary.month == get_month_name(txn.transaction_date.month)
    assert summary.year == str(txn.transaction_date.year)
    assert summary.account_id == txn.account_id
    assert summary.transactions_ids == [txn.id]
    assert summary.balance == txn.amount
    assert summary.transactions == 1
    assert summary.average_credit
    assert summary.average_debit == Decimal(0)
