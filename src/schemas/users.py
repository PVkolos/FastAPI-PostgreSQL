from typing import Annotated, TYPE_CHECKING
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from . import Task


class CreateUser(BaseModel):
    name: Annotated[str, Field(..., title="Имя пользователя", min_length=4, max_length=100)]
    age: Annotated[int, Field(..., title="Возраст пользователя", ge=1, le=130)]
    password: Annotated[str, Field(..., title="Пароль пользователя")]
    role: Annotated[str, Field(..., title='Роль пользователя')] #todo enum из моделей перенести куда-то и тут его использовать


class User(CreateUser):
    id: int
    tasks: list["Task"]
