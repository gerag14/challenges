from sqlalchemy import Column, ForeignKey, Index, String

from db.base_model import Base


class Transaction(Base, table=True):
    account_id = Column(ForeignKey("account.id"), nullable=False)
    account_number = Column(String(22), nullable=False)
    account_name = Column(String(150), nullable=False)

    __table_args__ = (
        Index(
            "id",
            "account_id",
        ),
    )
