from fastapi import APIRouter

from .files import router_files
from .tasks import router_tasks
from .users import router_users

router_main = APIRouter()

router_main.include_router(router_files)
router_main.include_router(router_tasks)
router_main.include_router(router_users)
