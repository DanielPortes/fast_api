from http import HTTPStatus

from tests.factories import TodoFactory


def test_create_todo(client, token):
    response = client.post(
        '/todo/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'test',
            'description': 'test',
            'state': 'draft',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'title': 'test',
        'description': 'test',
        'state': 'draft',
    }


def test_create_todo_should_return_success(client, token, session):
    response = client.post(
        '/todo/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'test',
            'description': 'test description',
            'state': 'draft',
        },
    )

    assert response.status_code == HTTPStatus.OK
    json_response = response.json()
    assert json_response['id'] > 0
    assert json_response['title'] == 'test'
    assert json_response['description'] == 'test description'
    assert json_response['state'] == 'draft'


def test_list_todos_should_return_5_todos(client, user, token, session):
    expected_todos = 5
    session.bulk_save_objects(TodoFactory.create_batch(expected_todos, user_id=user.id))
    session.commit()

    response = client.get(
        '/todo/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


def test_list_todos_should_return_1_todo(client, user, token, session):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()

    response = client.get(
        '/todo/?limit=1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == 1


def test_list_todos_should_return_5_todos_with_description(
    client, user, token, session
):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(
            expected_todos, user_id=user.id, description='description'
        )
    )
    session.commit()

    response = client.get(
        '/todo/?description=desc',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


def test_list_todos_should_return_1_todo_with_offset(client, user, token, session):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()

    response = client.get(
        '/todo/?offset=1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == 0


def test_list_todos_should_return_1_todo_with_limit(client, user, token, session):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()

    response = client.get(
        '/todo/?limit=1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == 1
    assert response.json()['todos'][0]['title'] == todo.title
    assert response.json()['todos'][0]['description'] == todo.description
    assert response.json()['todos'][0]['state'] == todo.state.name
    assert response.json()['todos'][0]['id'] == todo.id


def test_list_todos_should_return_1_todo_with_offset_and_limit(
    client, user, token, session
):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()

    response = client.get(
        '/todo/?offset=1&limit=1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == 0


def test_list_todos_should_return_1_todo_with_state_and_offset_and_limit(
    client, user, token, session
):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()

    response = client.get(
        f'/todo/?state={todo.state.name}&offset=1&limit=1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == 0


def test_patch_todo_error(client, token):
    response = client.patch(
        '/todo/10',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}


def test_patch_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()

    response = client.patch(
        f'/todo/{todo.id}',
        json={'title': 'new title'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'new title'


def test_delete_todo_error(client, token):
    response = client.delete(
        '/todo/10',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}


def test_delete_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()

    response = client.delete(
        f'/todo/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Task deleted'}
