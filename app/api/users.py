from typing import Optional

from fastapi_users import BaseUserManager, FastAPIUsers, IntegerIDMixin, schemas, models, exceptions
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from starlette.requests import Request

from app import database
from app.database import db_session
from app.interaction import User
from config import jwt_secret

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        async with db_session() as session:
            existing_user = await database.select_model(session, User, User.username == user_create.username)
            if existing_user is not None:
                raise exceptions.UserAlreadyExists()
        return await super().create(user_create, safe, request)


async def get_user_manager():
    async with db_session() as session:
        yield UserManager(SQLAlchemyUserDatabase(session, User))


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=jwt_secret, lifetime_seconds=60 * 60 * 24 * 30)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_user = fastapi_users.current_user(active=True)
