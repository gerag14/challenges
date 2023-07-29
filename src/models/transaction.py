from sqlalchemy import Column, DateTime, ForeignKey, Index, Numeric
from sqlalchemy.orm import relationship

from db.base_model import Base


class Transaction(Base, table=True):
    account_id = Column(ForeignKey("account.id"), nullable=False)
    amount = Column(Numeric(32, 2), nullable=False)
    transaction_date = Column(DateTime(timezone=False), nullable=False)
    # relationship
    account = relationship("Account", back_populates="transactions")

    __table_args__ = (
        Index(
            "id",
            "account_id",
        ),
    )
