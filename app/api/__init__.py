from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from app.api.users import fastapi_users
from . import users, scores, beatmaps, teams
from .schemas.user import UserUpdate, UserBase, UserWrite, UserRead

model_router = APIRouter(default_response_class=ORJSONResponse)

model_router.include_router(scores.router)
model_router.include_router(beatmaps.router)
model_router.include_router(teams.router)

router = APIRouter()

user_router = fastapi_users.get_users_router(UserRead, UserUpdate)
user_router.include_router(users.router_extends)

router.include_router(fastapi_users.get_auth_router(users.auth_backend), prefix="/auth/jwt", tags=["auth"])
router.include_router(user_router, prefix="/users", tags=["users"])
router.include_router(fastapi_users.get_register_router(UserBase, UserWrite), prefix="/auth", tags=["auth"])
router.include_router(model_router)


