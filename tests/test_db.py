from fast_api.models import User, mapper_registry
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


def test_create_user():
    engine = create_engine('sqlite:///:memory:')
    mapper_registry.metadata.create_all(engine)

    with Session(engine) as session:
        user = User(username='test', email='teste@teste.com', password='123456')
        session.add(user)
        session.commit()

    assert user.username == 'test'
