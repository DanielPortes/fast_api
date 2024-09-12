from http import HTTPStatus


def test_read_root_deve_retornar_mensagem_hello_world(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello, World!'}
