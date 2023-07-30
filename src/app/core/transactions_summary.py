from sqlalchemy.orm import Session

from app.crud.crud_transaction import crud_transaction
from app.schemas.schema_summary import SchemaMonthSummary, SchemaSummary
from app.utils import month_name


class TransactionsSummaryIterator:
    def __init__(self, data):
        self.data = data
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.data):
            value = self.data[self.index]
            self.index += 1
            return value
        else:
            raise StopIteration


class TransactionsSummary:
    def __init__(self, db: Session):
        self._db = db
        self.data = []

    def create_summary(self):
        summary_db = crud_transaction.get_transaction_summary(db=self._db)
        summary_data = self.create_month_summary(summary_db)
        return summary_data

    def create_month_summary(self, summary_db) -> SchemaSummary:
        summary = []
        for month in summary_db:
            month_summary = SchemaMonthSummary(
                balance=month.balance,
                transactions=month.transactions,
                average_debit=month.average_debit,
                average_credit=month.average_credit,
                month=month_name[month.month],
                year=str(month.year),
            )
            summary.append(month_summary)
        return SchemaSummary(months_summary=summary)

    def add_item(self, item):
        self.data.append(item)

    def __iter__(self):
        return TransactionsSummaryIterator(self.data)
