from datetime import timedelta, datetime
from jwt import encode, decode
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi import Depends
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from zoneinfo import ZoneInfo
from fast_api.database import get_session
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

SECRET_KEY = 'd1b3e7'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
        session: Session = Depends(get_session),
        token: str = Depends(oauth2_scheme),
):
    payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    email: str = payload.get('sub')

