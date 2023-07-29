from typing import Optional

from app.crud.base import CRUDBase
from app.models.Account import Account
from app.schemas.Account import AccountCreateSchema, AccountUpdateSchema
from sqlalchemy.orm import Session


class CRUDAccount(CRUDBase[Account, AccountCreateSchema, AccountUpdateSchema]):
    def get_by_account_number(
        self, db: Session, *, account_number: str
    ) -> Optional[Account]:
        return (
            db.query(Account).filter(Account.account_number == account_number).first()
        )


crud_Account = CRUDAccount(Account)
