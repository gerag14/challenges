from typing import Generator

import pytest

from db.base_model import BaseModel
from db.init_db import init_db
from db.session import SessionLocal, engine


@pytest.fixture(scope="session")
def db() -> Generator:
    BaseModel.metadata.drop_all(bind=engine)
    BaseModel.metadata.create_all(bind=engine)
    session = SessionLocal()
    init_db()
    yield session
