import csv

from sqlalchemy.orm import Session

from app.crud.crud_account import crud_account
from app.schemas.schema_account import SchemaAccountCreate


def init_db(db: Session) -> None:
    # initialising the database with some data to challenge
    init_accounts(db)


def init_accounts(db: Session) -> None:
    network = crud_account.get_multi(db, limit=1)
    if len(network) > 0:
        return None

    with open("./static_root/accounts/initial_accounts.csv", newline="") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader)
        data = list(reader)
        for row in data:
            if row:
                cypto = SchemaAccountCreate(
                    account_number=row[0],
                    account_name=row[1],
                )
                crud_account.create(db, obj_in=cypto)  # n
