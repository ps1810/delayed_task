from fastapi import APIRouter

from .tasks import router as tasks_router


router = APIRouter(prefix="/v1")
router.include_router(tasks_router)