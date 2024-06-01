from fastapi import APIRouter

from users import router as users_router
from osu import router as osu_router

router = APIRouter()

router.include_router(users_router)
router.include_router(osu_router)
