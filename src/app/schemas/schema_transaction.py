from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class SchemaTransactionBase(BaseModel):
    account_id: int
    transaction_date: date
    amount: Decimal


class SchemaTransactionCreate(SchemaTransactionBase):
    pass


class SchemaTransactionUpdate(BaseModel):
    account_id: int
    notified: bool


class SchemaTransaction(SchemaTransactionBase):
    id: int
    notified: bool

    class Config:
        orm_mode = True
