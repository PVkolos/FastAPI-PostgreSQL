from typing import Annotated, List, Dict
from fastapi import APIRouter, Body
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm

# from schemas.users import CreateUser, User
from src.schemas.users import CreateUser, User
from src.schemas.auth_schemas import TokenInfo
from src.database.database_orm import DataBase
# from api.auth import utils
from .auth import utils

router_users = APIRouter()


@router_users.post('/users/add', tags=['Работа с пользователями'], summary='Добавление пользователя в бд')
async def add_user(user: Annotated[CreateUser, Body(..., example={
                                                                    "age": "возраст пользователя",
                                                                    "name": "Имя пользователя",
                                                                    "password": "Пароль",
                                                                })]) -> Dict[str, int]:

    await DataBase.insert_user(user.name, user.age, utils.hash_password(user.password))
    return {'response': 200}


@router_users.get('/users', tags=['Работа с пользователями'], summary='Список всех пользователей с БД')
async def get_users_all() -> List[User]:
    list_users = await DataBase.get_all_users()
    return list_users


@router_users.post('/users/login',
                   tags=['Работа с пользователями'],
                   summary='Войти в аккаунт (выпустить токен)',
                   response_model=TokenInfo)
async def login_user(
        user: User = Depends(utils.validate_user_login)
    ) -> TokenInfo:
    payload = {
        'sub': user.id,
        'name': user.name,
        'age': user.age,
        'iat': ...,
        'exp': ...
    }
    access_token = utils.encode_jwt(payload)
    return TokenInfo(access_token=access_token, token_type='Bearer')


# @router_users.get('/users/check_auth', tags=['Работа с пользователями'], summary='Проверка авторизации')
# async def check_auth(user: User = Depends(utils.check_auth)) -> Dict:
#     return {'response': 200, 'name': user.name}

@router_users.get('/users/check_auth', tags=['Работа с пользователями'], summary='Проверка авторизации')
async def check_auth(user: Annotated[User, Depends(utils.check_auth)]) -> Dict:
    return {'response': 200, 'name': user.name}
