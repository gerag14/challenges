from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Index, Numeric, String
from sqlalchemy.orm import relationship

from db.base_model import BaseModel


class Transaction(BaseModel):
    account_id = Column(ForeignKey("account.id"), nullable=False)
    importfile_id = Column(ForeignKey("importfile.id"), nullable=False)
    transaction_import_id = Column(String(100), nullable=False)
    amount = Column(Numeric(32, 2), nullable=False)
    transaction_date = Column(DateTime(timezone=False), nullable=False)
    notified = Column(Boolean, default=False)
    # relationship
    account = relationship("Account", back_populates="transactions")
    importfile = relationship("ImportFile", back_populates="transactions")

    __table_args__ = (
        Index(
            "idx_id_account_id",
            "id",
            "account_id",
        ),
    )
