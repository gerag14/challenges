from pydantic import BaseModel

from .schema_transaction import SchemaTransaction


class SchemaAccountBase(BaseModel):
    account_number: str
    account_name: str


class SchemaAccountCreate(SchemaAccountBase):
    pass


class SchemaAccountUpdate(SchemaAccountBase):
    pass


class SchemaAccount(SchemaAccountBase):
    id: int
    transactions: list[SchemaTransaction] = []

    class Config:
        orm_mode = True
