from typing import Annotated, List, Dict, TYPE_CHECKING
from fastapi import APIRouter, Body, HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.schemas import CreateUser, User, TokenInfo
from src.database.database_orm import DataBase
# from api.auth import utils
from .auth import utils
from src.config import settings

router_users = APIRouter()


@router_users.post('/users/add', tags=['Работа с пользователями'], summary='Добавление пользователя в бд')
async def add_user(user: Annotated[CreateUser, Body(..., example={
                                                                    "age": "возраст пользователя",
                                                                    "name": "Имя пользователя",
                                                                    "password": "Пароль",
                                                                    "role": "Роль пользователя"
                                                                })],
                   # creator: Annotated[User, Depends(utils.check_is_admin)]
                   ) -> Dict[str, int | str]:
    # if user.role not in settings.roles.dict():
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Неверная роль пользователя")
    await DataBase.insert_user(user.name, user.age, utils.hash_password(user.password), user.role)
    # return {'response': 200, 'creator': creator.name}
    return {'response': 200, }


@router_users.get('/users', tags=['Работа с пользователями'], summary='Список всех пользователей с БД')
async def get_users_all(user: Annotated[User, Depends(utils.check_is_admin)]) -> List[User]:
    list_users = await DataBase.get_all_users()
    return list_users


@router_users.post('/users/login',
                   tags=['Работа с пользователями'],
                   summary='Войти в аккаунт (выпустить токен)',
                   response_model=TokenInfo, response_model_exclude_none=True)
async def login_user(
        user: User = Depends(utils.validate_user_login)
    ) -> TokenInfo:

    access_token = utils.create_access_jwt(user)
    refresh_token = utils.create_refresh_jwt(user)
    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


# @router_users.get('/users/check_auth', tags=['Работа с пользователями'], summary='Проверка авторизации')
# async def check_auth(user: User = Depends(utils.check_auth)) -> Dict:
#     return {'response': 200, 'name': user.name}


@router_users.get('/users/check_auth', tags=['Работа с пользователями'], summary='Проверка авторизации')
async def check_auth(user: Annotated[User, Depends(utils.check_token_auth)]) -> Dict:
    return {'response': 200, 'name': user.name}


@router_users.post('/users/generate-access', tags=['Работа с пользователями'], summary='Перевыпуск access jwt',
                   response_model=TokenInfo, response_model_exclude_none=True)
async def generate_access_jwt(user: User = Depends(utils.check_token_auth_refresh)):
    return TokenInfo(access_token=utils.create_access_jwt(user=user))
