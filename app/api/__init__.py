from fastapi import APIRouter

from app.api.users import fastapi_users
from . import users, scores, beatmaps
from .schemas.users import UserUpdate, UserBase, UserWrite, UserRead

router = APIRouter()

router.include_router(fastapi_users.get_auth_router(users.auth_backend), prefix="/auth/jwt", tags=["auth"])
router.include_router(fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/users", tags=["users"])
router.include_router(fastapi_users.get_register_router(UserBase, UserWrite), prefix="/auth", tags=["auth"])

router.include_router(scores.router)
router.include_router(beatmaps.router)
