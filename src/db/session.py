from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autoflush=False, bind=engine)


@contextmanager
def get_db():
    session = SessionLocal()
    try:
        yield session
    except Exception as error:
        session.close()
        raise Exception(error)
    finally:
        session.close()


@contextmanager
def atomic_transaction(db: Session):
    session = db
    transaction = None
    try:
        transaction = session.begin_nested()
        yield session
        if transaction.is_active:
            transaction.commit()
    except Exception as error:
        if transaction is not None:
            transaction.rollback()  # Deshacer los cambios en la base de datos
        raise Exception(error)
