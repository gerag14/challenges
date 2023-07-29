import csv
import logging

from sqlalchemy.orm import Session

from app.crud.crud_account import crud_account
from app.schemas.schema_account import SchemaAccountCreate
from db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db() -> None:
    # initialising the database with some data to challenge
    logger.info("Connecting..")
    db = SessionLocal()
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
                    email=row[2],
                )
                crud_account.create(db, obj_in=cypto)  # n


def main() -> None:
    logger.info("Creating initial data")
    init_db()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
