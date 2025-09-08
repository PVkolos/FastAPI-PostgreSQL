from typing import Annotated

from sqlalchemy import create_engine, inspect, insert, select, update, delete
from models import metadata_obj, users, tasks

from config import settings

sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=False,
    pool_size=5,
    max_overflow=10,
)

def table_is_exists(name: str) -> bool:
    ins = inspect(sync_engine)
    ret = ins.dialect.has_table(sync_engine.connect(), name)
    return ret


def create_table(table, engine):
    with engine.begin() as connection:
        if not table_is_exists(table.name):
            table.create(connection)
            print(f'INFO: Table "{table}" created')
        else:
            print(f'INFO: Table "{table}" already exists')


def insert_info():
    with sync_engine.begin() as conn:
        st = insert(users).values(username='root', name='alex')
        conn.execute(st)

def create_user(username, name):
    with sync_engine.begin() as conn:
        st = insert(users).values(username=username, name=name)
        conn.execute(st)


def create_task(author_id, title, description):
    with sync_engine.begin() as conn:
        st = insert(tasks).values(author_id=author_id, title=title, description=description)
        conn.execute(st)


def get_tasks_all_db():
    with sync_engine.begin() as conn:
        query = select(tasks)
        return conn.execute(query)


def get_users_all_db():
    with sync_engine.begin() as conn:
        query = select(users)
        return conn.execute(query).fetchall()


def get_tasks_user_db(id_user: int) -> list[dict]:
    with sync_engine.begin() as conn:
        query = select(tasks).where(tasks.c.author_id == id_user)
        return conn.execute(query).fetchall()


def update_task(task_id: int, status: str) -> int:
    with sync_engine.begin() as conn:
        st = update(tasks).where(tasks.c.id == task_id).values(status=status)
        result = conn.execute(st)
        return result.rowcount


def delete_task_db(task_id: int) -> int:
    with sync_engine.begin() as conn:
        query = delete(tasks).where(tasks.c.id == task_id)
        res = conn.execute(query)
        return res.rowcount


create_table(users, sync_engine)
create_table(tasks, sync_engine)
# insert_info()

