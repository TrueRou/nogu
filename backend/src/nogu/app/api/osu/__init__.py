from fastapi import APIRouter

from . import scores, stages, teams, beatmaps

router = APIRouter(prefix="/osu")

router.include_router(scores.router)
router.include_router(beatmaps.router)
router.include_router(teams.router)
router.include_router(stages.router)
