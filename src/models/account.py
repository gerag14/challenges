from sqlalchemy import Column, Index, String

from db.base_model import Base


class Account(Base, table=True):
    account_number = Column(String(22), nullable=False)
    account_name = Column(String(150), nullable=False)

    __table_args__ = (
        Index(
            "account_number",
        ),
    )
