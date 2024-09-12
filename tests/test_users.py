from http import HTTPStatus

from fast_api.schemas import UserPublic


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'test',
            'email': 'teste@teste.com',
            'password': '123',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'test',
        'email': 'teste@teste.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'test2',
            'email': 'testusername@teste.com',
            'password': '654321',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': 'test2',
        'email': 'testusername@teste.com',
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_update_user_with_wrong_user(client, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'test2',
            'email': 'teste@teste.com',
            'password': '654321',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_delete_user_with_wrong_user(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


# -------------------------------------------------------------------------------------------------------------------
# def test_create_user_should_return_400_email_exists(client, user):
#     response = client.post(
#         '/users/',
#         json={
#             'username': 'test2',
#             'email': 'tete@tete.com',
#             'password': '123',
#         },
#     )
#     assert response.status_code == HTTPStatus.CONFLICT
#     assert response.json() == {'detail': 'Email already exists'}
#
#
# def test_create_user_should_return_400_username_exists(client, user):
#     response = client.post(
#         '/users/',
#         json={
#             'username': user.username,
#             'email': 'daniel@teste.com',
#             'password': '123',
#         },
#     )
#     assert response.status_code == HTTPStatus.CONFLICT
#     assert response.json() == {'detail': 'Username already exists'}
#
#
# def test_delete_user_should_return_not_found(client):
#     response = client.delete('/users/333')
#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {'detail': 'User not found'}
#
#
# def test_get_user_should_return_not_found(client):
#     response = client.get('/users/999')
#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {'detail': 'User not found'}
#
# def test_update_user_should_return_not_found(client, user, token):
#     response = client.put(
#         f'/users/{user.id + 100}',
#         headers={'Authorization': f'Bearer {token}'},
#         json={
#             'id': 901,
#             'username': 'test901',
#             'email': 'testusername901@teste.com',
#             'password': '654321',
#         },
#     )
#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {'detail': 'User not found'}


def test_get_user(client, user):
    response = client.get(f'/users/{user.id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': user.username,
        'email': user.email,
    }
