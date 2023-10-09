from fastapi import APIRouter

from app.api.internal import scores, stages, teams, beatmaps, oauth

router = APIRouter()

router.include_router(scores.router)
router.include_router(beatmaps.router)
router.include_router(teams.router)
router.include_router(stages.router)
router.include_router(oauth.router)
