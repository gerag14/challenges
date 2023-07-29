from typing import Generator

import pytest

from app.initial_data import main as init_db
from db.base_model import BaseModel
from db.session import SessionLocal, engine


@pytest.fixture(scope="session")
def db() -> Generator:
    BaseModel.metadata.drop_all(bind=engine)
    BaseModel.metadata.create_all(bind=engine)
    session = SessionLocal()
    init_db()
    yield session
