from enum import Enum

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, func
import datetime
from src.database.models import Base
from src.enums import Status


class TaskModel(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[Status] = mapped_column(nullable=False, server_default="in_progress")
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    # created_at: Mapped[datetime.datetime] = mapped_column(server_default=datetime.datetime.utcnow)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), onupdate=datetime.datetime.utcnow)

    user: Mapped["UserModel"] = relationship(back_populates="tasks")

    repr_cols = ('author_id', )