import asyncio

from sqlalchemy import select, delete
from database.create_session import async_engine, async_session
from database.models.tasks_model import TaskModel
from database.models.users_model import UserModel
from database.models.base_model import Base

from sqlalchemy.orm import selectinload, contains_eager
from schemas.users import User
from schemas.tasks import Task


class DataBase:
    @staticmethod
    async def create_table():
        async with async_engine.begin() as connection:
            # await connection.run_sync(Base.metadata.drop_all)
            await connection.run_sync(Base.metadata.create_all)

    @staticmethod
    async def insert_user(name, age, password):
        user = UserModel(name=name, age=age, password=password)
        async with async_session() as session:
            session.add(user)
            await session.commit()

    @staticmethod
    async def insert_task(title, description, author_id):
        user = TaskModel(title=title, description=description, author_id=author_id)
        async with async_session() as session:
            session.add(user)
            await session.commit()

    @staticmethod
    async def select_task():
        async with async_session() as session:
            query = select(TaskModel)
            result = await session.execute(query)
            # print(result)
            tasks = result.scalars().all()
            return tasks

    @staticmethod
    async def update_task(task_id, new_status):
        async with async_session() as session:
            task = await session.get(TaskModel, task_id)
            task.status = new_status
            await session.commit()

    @staticmethod
    async def select_task_from_user():
        async with async_session() as session:
            query = (
                select(UserModel)
                # .options(selectinload(UserModel.tasks))
                .join(TaskModel, UserModel.id == TaskModel.author_id)
                .options(selectinload(UserModel.tasks))
                # .options(contains_eager(UserModel.tasks))
                # .filter(TaskModel.title == 'task1')
            )
            res = await session.execute(query)
            result = res.unique().scalars().all()

            tasks1 = result[0]
            print(tasks1)

    @staticmethod
    async def get_all_users():
        async with async_session() as session:
            query = (
                select(UserModel)
                .options(selectinload(UserModel.tasks))
            )
            res = await session.execute(query)
            result = res.unique().scalars().all()
            return [User.model_validate(var, from_attributes=True) for var in result]

    @staticmethod
    async def get_all_tasks():
        async with async_session() as session:
            query = (
                select(TaskModel)
            )
            result = await session.execute(query)
            result = result.scalars().all()
            return [Task.model_validate(var, from_attributes=True) for var in result]

    @staticmethod
    async def get_tasks_definite_user(user_id):
        async with async_session() as session:
            query = (
                select(TaskModel)
                .filter(TaskModel.author_id == user_id)
            )
            result = await session.execute(query)
            result = result.scalars().all()
            return [Task.model_validate(var, from_attributes=True) for var in result]

            # ---- требуется доп валидация id для использования метода ниже ----
            # query = (
            #     select(UserModel)
            #     .options(selectinload(UserModel.tasks))
            #     .filter(UserModel.id == id_)
            # )
            # res = await session.execute(query)
            # result = res.scalars().first()
            # return result.tasks

    @staticmethod
    async def delete_task(task_id):
        async with async_session() as session:
            task = await session.get(TaskModel, task_id)
            await session.delete(task)
            await session.commit()

    @staticmethod
    async def get_user(user_id: int):
        async with async_session() as session:
            query = (
                select(UserModel)
                .where(UserModel.id == user_id)
            )
            res = await session.execute(query)
            result = res.scalars().first()
            return result


# asyncio.run(create_table())
# asyncio.run(insert_user('polp', 121))
# asyncio.run(insert_user('pvkolos', 20))
# asyncio.run(insert_task('task1', 'desc1', 1))
# asyncio.run(insert_task('task2', 'desc2', 1))
# asyncio.run(test_user())

# asyncio.run(DataBase.create_table())
# asyncio.run(DataBase.insert_user('name2', 121))
# asyncio.run(DataBase.insert_user('namу3', 112))
# asyncio.run(DataBase.insert_task('task1', 'description1', 1))
# asyncio.run(DataBase.update_task(1, 'done'))
