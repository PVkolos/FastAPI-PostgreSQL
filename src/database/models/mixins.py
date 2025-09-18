import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import (
    declared_attr,
    mapped_column,
    Mapped,
    relationship
)

if TYPE_CHECKING:
    from src.database.models import UserModel


class UserRelationMixin:
    _author_id_ondelete: str = "CASCADE"
    _back_populates: str = None

    @declared_attr
    def author_id(cls) -> Mapped[int]:
        return mapped_column(ForeignKey("users.id", ondelete=cls._author_id_ondelete))

    @declared_attr
    def created_at(cls) -> Mapped[datetime.datetime]:
        return mapped_column(server_default=func.now())

    @declared_attr
    def updated_at(cls) -> Mapped[datetime.datetime]:
        return mapped_column(server_default=func.now(), onupdate=datetime.datetime.utcnow)

    @declared_attr
    def user(cls) -> Mapped["UserModel"]:
        return relationship(back_populates=cls._back_populates)
