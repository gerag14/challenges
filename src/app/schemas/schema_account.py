from pydantic import BaseModel

from .transaction import Transaction


class SchemaAccountBase(BaseModel):
    account_number: str
    account_name: str


class SchemaAccountCreate(SchemaAccountBase):
    pass


class SchemaAccount(SchemaAccountBase):
    id: int
    transactions: list[Transaction] = []

    class Config:
        orm_mode = True
