from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.account import Account
from app.schemas.schema_account import SchemaAccountCreate, SchemaAccountUpdate

from .crud_base import CRUDBase


class CRUDAccount(CRUDBase[Account, SchemaAccountCreate, SchemaAccountUpdate]):
    def get_by_account_number(self, db: Session, *, account_number: str) -> Optional[Account]:
        return db.query(Account).filter(Account.account_number == account_number).first()

    def get_multi_not_notified(self, db: Session) -> List[Account]:
        return db.query(self.model).join(Account.transactions).filter_by(notified=False).all()


crud_account = CRUDAccount(Account)
