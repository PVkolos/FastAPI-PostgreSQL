from enum import Enum


class Role(Enum):
    user = "user"
    admin = "admin"


class Status(Enum):
    in_progress = "in_progress"
    done = "done"
    failed = "failed"