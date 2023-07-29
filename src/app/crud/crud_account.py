from typing import Optional

from sqlalchemy.orm import Session

from app.models.Account import Account
from app.schemas.Account import AccountCreateSchema, AccountUpdateSchema

from .crud_base import CRUDBase


class CRUDAccount(CRUDBase[Account, AccountCreateSchema, AccountUpdateSchema]):
    def get_by_account_number(
        self, db: Session, *, account_number: str
    ) -> Optional[Account]:
        return (
            db.query(Account).filter(Account.account_number == account_number).first()
        )


crud_Account = CRUDAccount(Account)
