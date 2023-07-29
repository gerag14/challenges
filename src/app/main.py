import logging

from app.core.transactions_summary import TransactionsSummary
from db.init_db import init_db
from db.session import SessionLocal


class ConsolidateSender:
    _db = None
    _consolidation_data = None
    _emails = None

    def load_consolidation_data(self):
        self._consolidation_data = TransactionsSummary(self._db).load_data()

    def send_emails(self):
        self._emails = self._consolidation_data

    def send_consolidation_emails(self) -> None:
        self._db = SessionLocal()
        logging.info("ConsolidateSender: accounts and transactions to send emails")
        self.load_consolidation_data()

        logging.info("Initialization of the email sending process")
        self.send_emails()


def main():
    init_db()
    consolidate_sender = ConsolidateSender()
    consolidate_sender.send_consolidation_emails()


if __name__ == "__main__":
    main()
