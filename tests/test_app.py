from http import HTTPStatus

def test_read_root_deve_retornar_mensagem_hello_world(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello, World!'}


def test_create_user_deve_retornar_usuario_criado(client):
    response = client.post('/users/', json={
        'username': 'test',
        'email': 'teste@teste.com',
        'password': '123456',
    })
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'test',
        'email': 'teste@teste.com',
        'id': 1,
    }
