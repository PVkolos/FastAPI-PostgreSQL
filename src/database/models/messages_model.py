from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base_model import Base
from src.enums import StatusMessage
from .mixins import UserRelationMixin


class MessageModel(UserRelationMixin, Base):
    __tablename__ = "messages"
    _author_id_ondelete = "SET NULL"
    _back_populates = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[StatusMessage] = mapped_column(nullable=False, server_default=StatusMessage.unmodified.value)
    text: Mapped[str] = mapped_column(nullable=False)
    repr_cols = ('author_id', )
