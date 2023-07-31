from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.account import Account
from app.models.transaction import Transaction
from app.schemas.schema_transaction import SchemaTransactionCreate, SchemaTransactionUpdate  # noqa

from .crud_base import CRUDBase


class CRUDTransaction(CRUDBase[Transaction, SchemaTransactionCreate, SchemaTransactionUpdate]):
    def get_by_transaction_import_id(self, db: Session, *, transaction_import_id: str) -> Optional[Transaction]:
        return db.query(self.model).filter_by(transaction_import_id=transaction_import_id).first()

    def get_by_importfile_id(self, db: Session, *, importfile_id: str) -> Optional[Transaction]:
        return db.query(self.model).filter_by(importfile_id=importfile_id).all()

    def get_multi_by_account_number(
        self,
        db: Session,
        *,
        account_number: str,
        offset: Optional[int] = 0,
        limit: Optional[int] = 100,
    ) -> List[Transaction]:
        return (
            db.query(self.model)
            .join(Transaction.account)
            .filter_by(account_number=account_number)
            .order_by(self.model.created_date.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

    def get_transaction_summary(self, db: Session):
        subquery_debit = (
            db.query(func.avg(Transaction.amount).label("average_debit"))
            .join(Account, Transaction.account_id == Account.id)
            .filter(Transaction.amount < 0, Transaction.notified.is_(False))
            .group_by(Account.id)
        )

        subquery_credit = (
            db.query(func.avg(Transaction.amount).label("average_credit"))
            .join(Account, Transaction.account_id == Account.id)
            .filter(Transaction.amount >= 0, Transaction.notified.is_(False))
            .group_by(Account.id)
        )

        transaction_summary = (
            db.query(
                Transaction.account_id,
                func.sum(Transaction.amount).label("balance"),
                func.count(Transaction.id).label("transactions"),
                func.coalesce(subquery_debit.as_scalar(), 0).label("average_debit"),
                func.coalesce(subquery_credit.as_scalar(), 0).label("average_credit"),
                func.avg(Transaction.amount).label("average_amount"),
                func.extract("month", Transaction.transaction_date).label("month"),
                func.extract("year", Transaction.transaction_date).label("year"),
                func.group_concat(Transaction.id).label("transaction_ids"),
            )
            .filter(Transaction.notified.is_(False))
            .group_by(
                Transaction.account_id,
                func.extract("month", Transaction.transaction_date),
                func.extract("year", Transaction.transaction_date),
            )
            .order_by(
                self.model.account_id.desc(),
                func.extract("month", Transaction.transaction_date),
                func.extract("year", Transaction.transaction_date),
            )
            .all()
        )

        return transaction_summary


crud_transaction = CRUDTransaction(Transaction)
