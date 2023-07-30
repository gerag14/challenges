import logging
import sys

from sqlalchemy.orm import Session

from app.core.import_transactions import ImportTransactions
from app.core.transactions_summary import TransactionsSummary
from db.init_db import init_db
from db.session import get_db


class ConsolidateSender:
    _db = None
    _consolidation_data = None
    _emails = None

    def __init__(self, db: Session, load_from_boto3: bool = False):
        self._boto3 = boto3
        self._db = db

    def import_data(self):
        ImportTransactions(self._db).import_transactions(load_from_boto3=self._boto3)

    def load_consolidation_data(self):
        self._consolidation_data = TransactionsSummary(self._db).load_data()

    def send_emails(self):
        self._emails = self._consolidation_data

    def send_consolidation_emails(self) -> None:
        logging.info("Import Transactions data from CSV files")
        self.import_data()

        logging.info("ConsolidateSender: accounts and transactions to send emails")
        self.load_consolidation_data()

        logging.info("Initialization of the email sending process")
        self.send_emails()


def main(load_from_boto3=False):
    init_db()
    with get_db() as db:
        consolidate_sender = ConsolidateSender(db, load_from_boto3=boto3)
        consolidate_sender.send_consolidation_emails()


if __name__ == "__main__":
    boto3 = False
    if len(sys.argv) > 1:
        # El primer argumento después del nombre del script (sys.argv[0]) es sys.argv[1]
        boto3 = sys.argv[1] == "boto3"

    main(load_from_boto3=boto3)
