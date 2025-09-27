from enum import Enum
from .config import Roles


# class Role(Enum):
#     user = "user"
#     admin = "admin"


Role = Enum('Role', Roles().dict())


class StatusTask(Enum):
    in_progress = "in_progress"
    done = "done"
    failed = "failed"


class StatusMessage(Enum):
    modified = "modified"
    unmodified = "unmodified"
    deleted = "deleted"
