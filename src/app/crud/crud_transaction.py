from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.schemas.schema_transaction import SchemaTransactionCreate, SchemaTransactionUpdate  # noqa

from .crud_base import CRUDBase


class CRUDTransaction(CRUDBase[Transaction, SchemaTransactionCreate, SchemaTransactionUpdate]):
    def get_by_transaction_import_id(self, db: Session, *, transaction_import_id: str) -> Optional[Transaction]:
        return db.query(self.model).filter_by(transaction_import_id=transaction_import_id).first()

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

    def get_multi_by_account_number_not_notified(
        self,
        db: Session,
        *,
        account_number: str,
        offset: Optional[int] = 0,
        limit: Optional[int] = 100,
    ) -> List[Transaction]:
        return (
            db.query(self.model)
            .filter_by(notified=False)
            .join(Transaction.account)
            .filter_by(
                account_number=account_number,
            )
            .order_by(self.model.created_date.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )


crud_transaction = CRUDTransaction(Transaction)
