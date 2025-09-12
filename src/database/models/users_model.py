from enum import Enum

from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.models import Base
from src.enums import Role


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    password: Mapped[bytes] = mapped_column(nullable=False)
    role: Mapped[Role] = mapped_column(nullable=False, server_default="user")

    tasks: Mapped[list["TaskModel"]] = relationship(back_populates="user")

    def __str__(self):
        return f'{self.__class__.__name__}({self.id=}, {self.name=}, {self.age=}, {self.role=})'