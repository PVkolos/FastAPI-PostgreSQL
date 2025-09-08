from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from database.database_orm import DataBase

from api import router_main


@asynccontextmanager
async def create_db_table(app: FastAPI):
    await DataBase.create_table()
    yield
    ...

app = FastAPI(lifespan=create_db_table)
app.include_router(router_main)


@app.get("/")
async def root() -> str:
    return 'Это тестовый проект для демонстрации навыков в FastAPI и PostgreSQL'


if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, reload=True)