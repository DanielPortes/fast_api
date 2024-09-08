import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_api.app import app
from fast_api.models import mapper_registry


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def session():
    engine = create_engine('sqlite:///:memory:')
    mapper_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    mapper_registry.metadata.drop_all(engine)
