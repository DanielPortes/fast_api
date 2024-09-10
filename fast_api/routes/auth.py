from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from http import HTTPStatus

from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fast_api.security import create_access_token, verify_password

from fast_api.database import get_session
from fast_api.models import User


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post('/token', response_model=Token)
def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: Session = Depends(get_session),
):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail='Incorrect username or password'
        )

    access_token = create_access_token(data={'sub': user.email})
    return {'access_token': access_token, 'token_type': 'Bearer'}


