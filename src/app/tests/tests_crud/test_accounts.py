from sqlalchemy.orm import Session

from app.crud.crud_account import crud_account
from app.schemas.schema_account import SchemaAccount, SchemaAccountCreate
from app.tests.utils import random_lower_string


def create_random_account(db: Session) -> SchemaAccount:
    random_1 = random_lower_string()
    random_2 = random_lower_string()
    account_in = SchemaAccountCreate(account_name=random_1, account_number=random_2)
    account = crud_account.create(db=db, obj_in=account_in)
    return account


def test_create_account(db: Session) -> None:
    account = create_random_account(db=db)
    assert account.account_name
    assert account.account_number


def test_get_account_by_number(db: Session):
    account = create_random_account(db=db)
    account_by_number = crud_account.get_by_account_number(db, account_number=account.account_number)
    assert account.account_number == account_by_number.account_number
