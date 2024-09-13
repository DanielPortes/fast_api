from http import HTTPStatus
from freezegun import freeze_time


def test_get_token(client, user):
    response = client.post(
        'auth/token',
        data={
            'username': user.email,
            'password': user.clean_password,
        },
    )
    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_token_expired_after_time(client, user):
    with freeze_time('2024-01-01 12:00:00'):
        response = client.post(
            'auth/token',
            data={
                'username': user.email,
                'password': user.clean_password,
            },
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2024-01-01 12:31:00'):
        response = client.put(
            f'users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            data={
                'username': 'nanana',
                'email': 'nanana@nanana.com',
                'password': 'nana123',
            },
        )
        token = response.json()
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert 'detail' in token
        assert token['detail'] == 'Could not validate credentials'


def test_refresh_token(client, user, token):
    response = client.post(
        'auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['access_token'] == token


def test_token_expired_dont_refresh(client, user):
    with freeze_time('2024-01-01 12:00:00'):
        response = client.post(
            'auth/token',
            data={
                'username': user.email,
                'password': user.clean_password,
            },
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2024-01-01 12:31:00'):
        response = client.post(
            'auth/refresh_token',
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json()['detail'] == 'Could not validate credentials'


def test_token_wrong_password(client, user):
    response = client.post(
        'auth/token',
        data={
            'username': user.email,
            'password': 'wrong_password',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'Incorrect username or password'

def test_token_inexistent_user(client):
    response = client.post(
        'auth/token',
        data={
            'username': 'inexistent_user@test.com',
            'password': 'wrong_password',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'Incorrect username or password'
