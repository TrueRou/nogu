from fastapi import APIRouter

from app.api.users import fastapi_users
from . import users, scores
from .schemas.users import UserFull, UserUpdate, UserBase

router = APIRouter()

router.include_router(fastapi_users.get_auth_router(users.auth_backend), prefix="/auth/jwt", tags=["auth"])
router.include_router(fastapi_users.get_users_router(UserFull, UserUpdate), prefix="/users", tags=["users"])
router.include_router(fastapi_users.get_register_router(UserBase, UserBase), prefix="/auth", tags=["auth"])

router.include_router(scores.router)