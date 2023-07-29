from typing import List, Optional

from app.crud.base import CRUDBase
from app.models.Transaction import Transaction
from app.schemas.Transaction import TransactionCreateSchema, TransactionUpdateSchema
from sqlalchemy.orm import Session


class CRUDTransaction(
    CRUDBase[Transaction, TransactionCreateSchema, TransactionUpdateSchema]
):
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


crud_transaction = CRUDTransaction(Transaction)
