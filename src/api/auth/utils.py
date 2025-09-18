import secrets
from datetime import datetime, timedelta
from typing import Annotated

import jwt
from src.config import settings
import bcrypt
from fastapi import HTTPException, status, Depends, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.database.database_orm import DataBase
from src.schemas import CreateTask
from src.schemas.users import User

# http_bearer = HTTPBearer()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/")


def encode_jwt(
        payload: dict,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
    ):
    encoded = jwt.encode(payload, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
        encoded: str | bytes,
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
    ):
    decoded = jwt.decode(encoded, public_key, algorithms=[algorithm])
    return decoded


def create_jwt(sub: int, payload: dict, token_type: str, expire: timedelta) -> str:
    payload['sub'] = sub
    payload[settings.const.TOKEN_TYPE_FIELD] = token_type
    payload['iat'] = datetime.utcnow()
    payload['exp'] = datetime.utcnow() + expire

    payload.update(payload)
    return encode_jwt(payload)


def create_access_jwt(user: User) -> str:
    payload = {
        'name': user.name,
        'age': user.age,
    }
    return create_jwt(
        sub=user.id,
        payload=payload,
        token_type=settings.const.TOKEN_ACCESS_FIELD,
        expire=settings.auth_jwt.access_token_expire_minutes,
    )


def create_refresh_jwt(user: User) -> str:
    payload = {}
    return create_jwt(
        sub=user.id,
        payload=payload,
        token_type=settings.const.TOKEN_REFRESH_FIELD,
        expire=settings.auth_jwt.refresh_token_expire_days,
    )


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
    ) -> dict:
    # token = creds.credentials
    try:
        payload = decode_jwt(encoded=token)
        return payload
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Инвалидный токен'
        )

# def check_token_auth(token_type: str = settings.const.TOKEN_ACCESS_FIELD) -> User:
#     async def check_token_jwt(payload: Annotated[dict, Depends(check_auth)],):
#         if payload.get(settings.const.TOKEN_TYPE_FIELD) != token_type:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token type not valid")
#         if user := await DataBase.get_user(payload.get("sub")):
#             return user
#
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Пользователь не найден')
#
#     return check_token_jwt


def validate_token_type(payload: dict, token_type: str) -> bool:
    print(token_type, payload.get(settings.const.TOKEN_TYPE_FIELD))
    if payload.get(settings.const.TOKEN_TYPE_FIELD) == token_type:
        return True
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token type not valid")


async def check_token_auth(
        payload: dict = Depends(check_auth)
) -> User:
    validate_token_type(payload, settings.const.TOKEN_ACCESS_FIELD)
    if user := await DataBase.get_user(payload.get("sub")):
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Пользователь не найден')


async def check_token_auth_refresh(
        payload: dict = Depends(check_auth)
) -> User:
    validate_token_type(payload, settings.const.TOKEN_REFRESH_FIELD)
    if user := await DataBase.get_user(payload.get("sub")):
        return user

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Пользователь не найден')


async def check_is_admin(user: Annotated[User, Depends(check_token_auth)]) -> User:
    if user.role.value != settings.roles.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет прав на выполнение операции!")
    return user


async def check_user_permission(task_id: int, user) -> bool:
    user_db = await DataBase.get_user_from_task_id(task_id)
    if user.id == user_db.id or await check_is_admin(user):
        return True
    return False
