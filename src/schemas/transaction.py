from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class TransactionBase(BaseModel):
    account_id: int
    transaction_date: date
    amount: Decimal


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: int

    class Config:
        orm_mode = True
