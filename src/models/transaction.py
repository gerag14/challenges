from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Index, Numeric
from sqlalchemy.orm import relationship

from db.base_model import Base


class Transaction(Base):
    account_id = Column(ForeignKey("account.id"), nullable=False)
    amount = Column(Numeric(32, 2), nullable=False)
    transaction_date = Column(DateTime(timezone=False), nullable=False)
    notified = Column(Boolean, default=False)
    # relationship
    account = relationship("Account", back_populates="transactions")

    __table_args__ = (
        Index(
            "id",
            "account_id",
        ),
    )
