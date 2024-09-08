from fast_api.models import User
from sqlalchemy import select


def test_create_user(session):
    user = User(username='test', email='teste@teste.com', password='123456')
    session.add(user)
    session.commit()

    result = session.scalar(select(User).where(User.email == 'teste@teste.com'))

    assert result.username == 'test'
