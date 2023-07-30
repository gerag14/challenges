from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from db.base_model import BaseModel


class ImportFile(BaseModel):
    file_name = Column(String(100), nullable=False)
    bucket_name = Column(String(50), nullable=False)
    processed = Column(Boolean, default=False)
    # relationship
    transactions = relationship("Transaction", back_populates="importfile")
