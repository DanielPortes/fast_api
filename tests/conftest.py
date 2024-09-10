import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_api.app import app
from fast_api.database import get_session
from fast_api.models import mapper_registry, User
from fast_api.security import get_password_hash


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    mapper_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    mapper_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    pwd = 'testtest'
    user = User(
        username='Teste', email='teste@test.com', password=get_password_hash(pwd)
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = pwd  # monkey patching
    return user
