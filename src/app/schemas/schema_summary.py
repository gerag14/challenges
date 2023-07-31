from decimal import Decimal

from pydantic import BaseModel


class SchemaMonthSummary(BaseModel):
    account_id: int
    transactions_ids: list[int]
    balance: Decimal
    transactions: int
    average_debit: Decimal
    average_credit: Decimal
    month: str
    year: str


class SchemaSummary(BaseModel):
    months_summary: list[SchemaMonthSummary]
