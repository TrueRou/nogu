from fastapi import APIRouter
from fastapi_users.schemas import BaseUser

from app.api.users import fastapi_users
from . import users, scores
from .schemas.users import UserFull, UserUpdate, UserCreate

router = APIRouter()

router.include_router(fastapi_users.get_auth_router(users.auth_backend), prefix="/auth/jwt", tags=["auth"])
router.include_router(fastapi_users.get_users_router(UserFull, UserUpdate), prefix="/users", tags=["users"])
router.include_router(fastapi_users.get_register_router(BaseUser, UserCreate), prefix="/auth", tags=["auth"])

router.include_router(scores.router)