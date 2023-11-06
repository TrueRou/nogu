from typing import Optional
from starlette.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from fastapi_users import BaseUserManager, FastAPIUsers, IntegerIDMixin, schemas, models, exceptions
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.router.common import ErrorCode
from sqlalchemy import or_
from starlette.requests import Request

from app import database
from app.database import db_session
from app.interaction import User
from app.api.schemas import APIException
from config import jwt_secret

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    async def get_by_ident(self, ident: str) -> Optional[models.UP]:
        async with db_session() as session:
            user =  await database.select_model(session, User, or_(User.username.like(ident), User.email == ident))
            if user is None:
                raise exceptions.UserNotExists()
            return user
        
    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        if (len(user_create.username) < 4 or len(user_create.username) > 16):
            raise APIException('Username illegal (Between: 4~16).', 'user.username.illegal')
        if (len(user_create.password) < 6):
            raise APIException('Password illegal (Above: 6).', 'user.password.illegal')
        if (len(user_create.country) != 2 or user_create.country.isalpha() == False):
            raise APIException('Country illegal.', 'user.country.illegal')

        async with db_session() as session:
            existing_user = await database.select_model(session, User, User.username.like(user_create.username))
            if existing_user is not None:
                raise exceptions.UserAlreadyExists()
        return await super().create(user_create, safe, request)
    
    async def authenticate(
        self, credentials: OAuth2PasswordRequestForm
    ) -> Optional[models.UP]:
        try:
            user = await self.get_by_ident(credentials.username)
        except exceptions.UserNotExists:
            # Run the hasher to mitigate timing attack
            # Inspired from Django: https://code.djangoproject.com/ticket/20760
            self.password_helper.hash(credentials.password)
            return None

        verified, updated_password_hash = self.password_helper.verify_and_update(
            credentials.password, user.hashed_password
        )
        if not verified:
            return None
        # Update password hash to a more robust one if needed
        if updated_password_hash is not None:
            await self.user_db.update(user, {"hashed_password": updated_password_hash})

        return user


async def get_user_manager():
    async with db_session() as session:
        yield UserManager(SQLAlchemyUserDatabase(session, User))


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=jwt_secret, lifetime_seconds=60 * 60 * 24 * 30)

def parse_exception(exception: HTTPException) -> APIException:
    if (exception.status_code == 500):
        return APIException('Backend server error.', 'glob.internal')
    if (exception.status_code == 401):
        return APIException('Unauthorized.', 'user.unauthorized')
    if (exception.status_code == 404):
        return APIException('Resources not found.', 'glob.not-exists')
    if (exception.status_code == 400):
        if (type(exception.detail) == dict):
            if (exception.detail['code'] in [ErrorCode.UPDATE_USER_INVALID_PASSWORD, ErrorCode.REGISTER_INVALID_PASSWORD, ErrorCode.RESET_PASSWORD_INVALID_PASSWORD]):
                return APIException('Illegal password format.', 'user.password.illegal', reason=exception.detail['reason'])
        if (exception.detail == ErrorCode.REGISTER_USER_ALREADY_EXISTS):
            return APIException('User already exists.', 'user.duplicated')
        if (exception.detail in [ErrorCode.LOGIN_BAD_CREDENTIALS, ErrorCode.RESET_PASSWORD_BAD_TOKEN]):
            return APIException('Incorrect username or password.', 'user.credentials.incorrect')
        if (exception.detail == ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS):
            return APIException('Email already exists.', 'user.email.duplicated')

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])