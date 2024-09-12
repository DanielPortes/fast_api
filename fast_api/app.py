from fastapi import FastAPI
from http import HTTPStatus

from fast_api.schemas import (
    Message,
)
from fast_api.routes import auth, users, todo

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todo.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello, World!'}
