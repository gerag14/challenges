from typing import Optional

from sqlalchemy.orm import Session

from app.models.account import Account
from app.schemas.schema_account import SchemaAccountCreate, SchemaAccountUpdate

from .crud_base import CRUDBase


class CRUDAccount(CRUDBase[Account, SchemaAccountCreate, SchemaAccountUpdate]):
    def get_by_account_number(
        self, db: Session, *, account_number: str
    ) -> Optional[Account]:
        return (
            db.query(Account).filter(Account.account_number == account_number).first()
        )


crud_account = CRUDAccount(Account)
