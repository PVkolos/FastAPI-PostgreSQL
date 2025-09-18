from sqlalchemy.orm import Mapped, mapped_column
from .base_model import Base
from src.enums import StatusTask
from .mixins import UserRelationMixin


class TaskModel(UserRelationMixin, Base):
    __tablename__ = "tasks"
    _author_id_ondelete = "CASCADE"
    _back_populates = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[StatusTask] = mapped_column(nullable=False, server_default=StatusTask.in_progress.value)

    repr_cols = ('author_id', )
