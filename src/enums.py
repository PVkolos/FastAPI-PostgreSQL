from enum import Enum
from src.config import Roles


# class Role(Enum):
#     user = "user"
#     admin = "admin"


Role = Enum('Role', Roles().dict())


class Status(Enum):
    in_progress = "in_progress"
    done = "done"
    failed = "failed"