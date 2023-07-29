from sqlalchemy import Column, Index, String
from sqlalchemy.orm import relationship

from db.base_model import Base


class Account(Base):
    account_number = Column(String(22), nullable=False)
    account_name = Column(String(150), nullable=False)
    # relationship
    transactions = relationship("Transaction", back_populates="account")

    __table_args__ = (
        Index(
            "account_number",
        ),
    )
