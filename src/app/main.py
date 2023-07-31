import argparse
import logging

from sqlalchemy.orm import Session

from app.core.import_transactions import ImportTransactions
from app.core.notify_transactions_summary import NotifyTransactionSummary
from app.core.transactions_summary import TransactionsSummary
from db.init_db import init_db
from db.session import get_db


class ConsolidateSender:
    _db = None
    _consolidation_data = None
    _emails = None

    def __init__(self, db: Session, aws_mode: bool = False):
        self._aws_mode = aws_mode
        self._db = db

    def import_data(self):
        ImportTransactions(self._db).import_transactions(load_from_boto3=self._aws_mode)

    def load_consolidation_data(self):
        self._consolidation_data = TransactionsSummary(self._db).create_summary()

    def send_emails(self):
        self._emails = NotifyTransactionSummary(db=self._db, data=self._consolidation_data).notify()

    def process(self) -> None:
        logging.info("Import Transactions data from CSV files")
        self.import_data()

        logging.info("ConsolidateSender: accounts and transactions to send emails")
        self.load_consolidation_data()

        logging.info("Initialization of the email sending process")
        self.send_emails()


def main(aws_mode=False):
    init_db()
    with get_db() as db:
        consolidate_sender = ConsolidateSender(db, aws_mode=aws_mode)
        consolidate_sender.process()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--aws", action="store_true", help="run AWS mode")
    args = parser.parse_args()

    main(aws_mode=args.aws)
