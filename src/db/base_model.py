from datetime import datetime

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id = Column(Integer, primary_key=True, index=True)
    created_date = datetime = Column(DateTime, default=datetime.utcnow)
    updated_date = datetime = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    __name__: str
    # Generate __tablename__ automatically

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
