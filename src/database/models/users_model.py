from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.models.base_model import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    password: Mapped[bytes] = mapped_column(nullable=False)

    tasks: Mapped[list["TaskModel"]] = relationship(back_populates="user")