from pydantic import BaseModel

from .transaction import Transaction


class AccountBase(BaseModel):
    account_number: str
    account_name: str


class AccountCreate(AccountBase):
    pass


class Account(AccountBase):
    id: int
    transactions: list[Transaction] = []

    class Config:
        orm_mode = True
