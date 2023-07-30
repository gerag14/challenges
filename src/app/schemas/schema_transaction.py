from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class SchemaTransactionBase(BaseModel):
    account_id: int
    importfile_id: int
    transaction_import_id: str
    transaction_date: date
    amount: Decimal


class SchemaTransactionCreate(SchemaTransactionBase):
    pass


class SchemaTransactionUpdate(BaseModel):
    notified: bool


class SchemaTransaction(SchemaTransactionBase):
    id: int
    notified: bool

    class Config:
        orm_mode = True
