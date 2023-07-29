from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class SchemaTransactionBase(BaseModel):
    account_id: int
    transaction_date: date
    amount: Decimal


class SchemaTransactionCreate(SchemaTransactionBase):
    pass


class SchemaTransaction(SchemaTransactionBase):
    id: int

    class Config:
        orm_mode = True
