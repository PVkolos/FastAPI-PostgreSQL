import datetime
from typing import Annotated

from pydantic import BaseModel, Field


class CreateTask(BaseModel):
    title: Annotated[str, Field(..., title="Название задачи", min_length=4, max_length=20)]
    description: Annotated[str, Field(..., title="Описание задачи", min_length=5, max_length=150)]
    author_id: Annotated[int, Field(..., title="id автора задачи", ge=1)]


class Task(CreateTask):
    id: int
    status: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
