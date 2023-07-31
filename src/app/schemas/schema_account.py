from pydantic import BaseModel, EmailStr

from .schema_transaction import SchemaTransaction


class SchemaAccountBase(BaseModel):
    account_number: str
    account_name: str
    email: EmailStr


class SchemaAccountCreate(SchemaAccountBase):
    pass


class SchemaAccountUpdate(SchemaAccountBase):
    pass


class SchemaAccount(SchemaAccountBase):
    id: int
    transactions: list[SchemaTransaction] = []

    class Config:
        orm_mode = True
