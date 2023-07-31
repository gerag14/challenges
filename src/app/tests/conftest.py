from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.base_model import BaseModel
from db.init_db import init_db

engine = create_engine("sqlite:///./db/tests_db.sqlite")
SessionTests = sessionmaker(autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db() -> Generator:
    BaseModel.metadata.drop_all(bind=engine)
    BaseModel.metadata.create_all(bind=engine)
    session = SessionTests()
    init_db()
    yield session
