from fast_api.models import User
from sqlalchemy import select

from tests.factories import TodoFactory


def test_create_user(session):
    user = User(username='test', email='teste@teste.com', password='123456')
    session.add(user)
    session.commit()

    result = session.scalar(select(User).where(User.email == 'teste@teste.com'))

    assert result.username == 'test'


def test_create_todo(session, user: User):
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    session.commit()
    session.refresh(todo)

    user = session.scalar(select(User).where(User.id == todo.user_id))
    assert todo in user.todos
