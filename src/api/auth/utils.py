from datetime import datetime, timedelta
from typing import Annotated

import jwt
from config import settings, auth_jwt
import bcrypt
from fastapi import Form, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database.database_orm import DataBase
from schemas.users import User

# http_bearer = HTTPBearer()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/")


def encode_jwt(
        payload: dict,
        private_key: str = auth_jwt.private_key_path.read_text(),
        algorithm: str = auth_jwt.algorithm,
        expire_minutes: int = auth_jwt.access_token_expire_minutes,
    ):
    payload['iat'] = datetime.utcnow()
    payload['exp'] = datetime.utcnow() + timedelta(minutes=expire_minutes)
    encoded = jwt.encode(payload, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
        encoded: str | bytes,
        public_key: str = auth_jwt.public_key_path.read_text(),
        algorithm: str = auth_jwt.algorithm,
    ):
    decoded = jwt.decode(encoded, public_key, algorithms=[algorithm])
    return decoded


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)


async def validate_user_login(
        # username: int | str = Form(..., title='ID пользователя'), password: str = Form(..., title='Пароль')
        # id_: str = Form(..., title='ID пользователя'), password: str = Form(..., title='Пароль')
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    id_ = form_data.username
    password = form_data.password

    if not (user := await DataBase.get_user(int(id_))):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Нет такого пользователя")
    if validate_password(password, user.password):
        return user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный пароль")


async def check_auth(
        token: str = Depends(oauth2_scheme)
        # creds: HTTPAuthorizationCredentials = Depends(http_bearer)
    ) -> User:
    # token = creds.credentials
    try:
        payload = decode_jwt(encoded=token)
        id_ = payload.get("sub")
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Инвалидный токен')
    if user := await DataBase.get_user(id_):
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Пользователь не найден')
