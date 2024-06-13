from fastapi import APIRouter

from .users import router as users_router
from .teams import router as teams_router
from .oauth import router as oauth_router
from .osu import router as osu_router

router = APIRouter()

router.include_router(users_router)
router.include_router(teams_router)
router.include_router(oauth_router)
router.include_router(osu_router)
