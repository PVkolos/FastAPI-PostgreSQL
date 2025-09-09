import asyncio
from typing import Annotated, Dict, List

import aiofiles
from fastapi import APIRouter, Body, Path, Query, HTTPException
from sqlalchemy.exc import IntegrityError, DBAPIError

from src.schemas import CreateTask, Task
from src.database.database_orm import DataBase

router_tasks = APIRouter()


@router_tasks.post('/tasks/add', tags=['Работа с задачами'], summary='Добавление задачи в БД пользователю')
async def add_task(task: Annotated[CreateTask, Body(..., example={
                                                        "author_id": "id автора поста",
                                                        "title": "название задачи",
                                                        "description": "описание задачи"
                                                    })]) -> Dict[str, int]:
    try:
        await DataBase.insert_task(task.title, task.description, task.author_id)
    except IntegrityError:
        raise HTTPException(404, "Автор с таким id не был найден!")
    return {'response': 200}


@router_tasks.get('/tasks', tags=['Работа с задачами'], summary='Список всех задач с БД')
async def get_tasks_all() -> List[Task]:
    list_tasks = await DataBase.get_all_tasks()
    return list_tasks


@router_tasks.get('/tasks/{user_id}', tags=['Работа с задачами'], summary='Получение всех задач конкретного пользователя')
async def get_tasks_user(user_id: Annotated[int, Path(..., title='id пользователя, задачи которого вы хотите получить')]) -> List[Task]:
    tasks = await DataBase.get_tasks_definite_user(user_id)
    return tasks


@router_tasks.put("/tasks/edit/{task_id}", tags=['Работа с задачами'], summary='Редактирование статуса задачи')
async def edit_task(task_id: Annotated[int, Path(..., title='id задачи, статус которой требуется изменить', ge=1)],
                    status: Annotated[str, Query(..., title='Статус задачи. Допустимые значения: in-progress, done, failed', max_length=11, min_length=4)]) -> Dict[str, int]:
    '''
    :param task_id: integer.
    \n:param status: string. Принимаемые значения: ['in_progress', 'done', 'failed']. Значение по умолчанию при создании таски: in_progress
    \n:return: None
    '''
    try:
        await DataBase.update_task(task_id, status)
        return {'response': 200}
    except DBAPIError:
        raise HTTPException(404, 'Задача принимает несуществующий статус. Прочтите в документации возможные статусы задач')
    except AttributeError:
        raise HTTPException(404, 'Несуществующая задача')


@router_tasks.delete('/tasks/delete/{task_id}', tags=['Работа с задачами'], summary='Удаление задачи')
async def delete_task(task_id: Annotated[int, Path(..., title='id задачи для удаления', ge=1)]) -> Dict[str, int]:
    await DataBase.delete_task(task_id)
    # count = delete_task_db(task_id)
    # if count == 0: raise HTTPException(404, 'Задача с таким id не найдена')
    return {'response': 200}


@router_tasks.get('/tasks/download/{user_id}', tags=['Работа с задачами'], summary='Фоновая выгрузка задач пользователя в файл')
async def tasks_to_file(user_id: Annotated[int, Path(..., title='id пользователя для выгрузки задач', ge=1)]) -> Dict[str, str]:
    asyncio.create_task(dump_tasks(user_id))
    return {'response': 'задача поставлена в очередь'}


async def dump_tasks(user_id):
    tasks = await DataBase.get_tasks_definite_user(user_id)
    async with aiofiles.open(f'files/dump_{user_id}.txt', 'w', encoding='utf-8') as file:
        for task in tasks: await file.write(f'{task.title} {task.description} {task.status}\n\n')


