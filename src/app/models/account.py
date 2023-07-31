from sqlalchemy import Column, Index, String
from sqlalchemy.orm import relationship

from db.base_model import BaseModel


class Account(BaseModel):
    account_number = Column(String(22), nullable=False)
    account_name = Column(String(150), nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    # relationship
    transactions = relationship("Transaction", back_populates="account")

    __table_args__ = (
        Index(
            "idx_account_number",
            "account_number",
        ),
    )
