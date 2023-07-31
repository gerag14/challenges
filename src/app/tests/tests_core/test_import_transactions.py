import uuid

from sqlalchemy.orm import Session

from app.core.import_transactions import ImportTransactions
from app.crud.crud_transaction import crud_transaction
from app.tests.tests_crud.test_accounts import create_random_account
from app.tests.tests_crud.test_import_file import create_random_import_file
from app.tests.utils import generate_random_amount, generate_random_date


def create_random_transactions(db):
    transactions = []
    account_number = create_random_account(db=db).account_number
    for i in range(3):
        txn = (
            str(uuid.uuid4()),
            account_number,
            generate_random_date(),
            generate_random_amount(),
        )
        transactions.append(txn)
    return transactions


def tests_load_data_from_csv(db: Session):
    import_file = create_random_import_file(db=db)
    data = create_random_transactions(db=db)
    ImportTransactions(db=db).load_data_from_csv(file_import=import_file, data=data)
    transactions_db = crud_transaction.get_by_importfile_id(db, importfile_id=import_file.id)
    assert transactions_db
    last_txn = transactions_db[-1]
    assert last_txn.importfile_id == import_file.id
