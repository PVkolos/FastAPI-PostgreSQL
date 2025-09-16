import asyncio
from typing import Annotated, Dict, List

import aiofiles
from fastapi import APIRouter, Body, Path, Query, HTTPException, Depends
from sqlalchemy.exc import IntegrityError, DBAPIError
from starlette import status

from src.schemas import CreateTask, Task, User
from src.database.database_orm import DataBase

from src.enums import Status
from .auth import utils
from src.config import settings

router_tasks = APIRouter()


@router_tasks.post('/tasks/add', tags=['Работа с задачами'], summary='Добавление задачи в БД пользователю')
async def add_task(task: Annotated[CreateTask, Body(..., example={
    "author_id": "id автора поста",
    "title": "название задачи",
    "description": "описание задачи"
})],
                   creator: Annotated[User, Depends(utils.check_auth)],
                   ) -> Dict[str, int]:
    try:
        if (creator.id == task.author_id) or (creator.role.value == settings.roles.admin):
            await DataBase.insert_task(task.title, task.description, task.author_id)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Вы можете создавать таски только себе")
    except IntegrityError:
        raise HTTPException(404, "Автор с таким id не был найден!")
    return {'response': 200}


@router_tasks.get('/tasks', tags=['Работа с задачами'], summary='Список всех задач с БД')
async def get_tasks_all(admin: Annotated[User, Depends(utils.check_is_admin)]) -> List[Task]:
    list_tasks = await DataBase.get_all_tasks()
    return list_tasks


@router_tasks.get('/tasks/{user_id}', tags=['Работа с задачами'],
                  summary='Получение всех задач конкретного пользователя')
async def get_tasks_user(
        user_id: Annotated[int, Path(..., title='id пользователя, задачи которого вы хотите получить')],
        user: Annotated[User, Depends(utils.check_auth)],
) -> List[Task]:
    if user.id == user_id or (user.role.value == settings.roles.admin):
        return await DataBase.get_tasks_definite_user(user_id)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Вы можете получить только свои таски!")


@router_tasks.put("/tasks/edit/{task_id}", tags=['Работа с задачами'], summary='Редактирование статуса задачи')
async def edit_task(task_id: Annotated[int, Path(..., title='id задачи, статус которой требуется изменить', ge=1)],
                    new_status: Annotated[
                        Status, Query(..., title='Статус задачи.')],
                    user: Annotated[User, Depends(utils.check_auth)],
                    ) -> Dict[str, int]:
    '''
    :param user:
    :param task_id: integer.
    :param new_status: string. Принимаемые значения: ['in_progress', 'done', 'failed']. Значение по умолчанию при создании таски: in_progress
    \n:return: None
    '''
    try:
        if await utils.check_user_permission(task_id, user):
            await DataBase.update_task(task_id, new_status)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Вы можете менять статус только своих тасок!")
        return {'response': 200}
    # except DBAPIError:
    #     raise HTTPException(404, 'Задача принимает несуществующий статус. Прочтите в документации возможные статусы задач')
    except AttributeError:
        raise HTTPException(404, 'Несуществующая задача')


@router_tasks.delete('/tasks/delete/{task_id}', tags=['Работа с задачами'], summary='Удаление задачи')
async def delete_task(task_id: Annotated[int, Path(..., title='id задачи для удаления', ge=1)],
                        user: Annotated[User, Depends(utils.check_auth)],
                      ) -> Dict[str, int]:
    if await utils.check_user_permission(task_id, user):
        await DataBase.delete_task(task_id)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Вы можете менять статус только своих тасок!")

    return {'response': 200}


@router_tasks.get('/tasks/download/{user_id}', tags=['Работа с задачами'], summary='Фоновая выгрузка задач пользователя в файл')
async def tasks_to_file(user_id: Annotated[int, Path(..., title='id пользователя для выгрузки задач', ge=1)]) -> Dict[str, str]:
    asyncio.create_task(dump_tasks(user_id))
    return {'response': 'задача поставлена в очередь'}


async def dump_tasks(user_id):
    tasks = await DataBase.get_tasks_definite_user(user_id)
    async with aiofiles.open(f'{settings.const.base_dir}/{settings.const.dump_path}/dump_{user_id}.txt', 'w', encoding='utf-8') as file:
        for task in tasks:
            await file.write(f'{task.title} {task.description} {task.status}\n\n')
