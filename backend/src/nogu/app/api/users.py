from typing import Optional
from fastapi import APIRouter
from sqlmodel import select
from starlette.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    IntegerIDMixin,
    schemas,
    models,
    exceptions,
)
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.router.common import ErrorCode
from sqlalchemy import or_
from starlette.requests import Request

from nogu.app.database import async_session, auto_session
from nogu.app.models import User
from nogu.app.constants.exceptions import APIException
from nogu.app.models.user import UserRead, UserUpdate, UserWrite
from config import jwt_secret

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
router = APIRouter()

user_unauthorized = APIException("Unauthorized.", "user.unauthorized")
user_duplicated = APIException("User already exists.", "user.duplicated")
user_username_illegal = APIException("Username illegal.", "user.username.illegal")
user_password_illegal = APIException("Password illegal.", "user.password.illegal")
user_country_illegal = APIException("Country illegal.", "user.country.illegal")
user_credentials_incorrect = APIException("Incorrect username or password.", "user.credentials.incorrect")
user_email_duplicated = APIException("Email already exists.", "user.email.duplicated")
user_internal = APIException("Backend server error.", "user.internal")
user_not_exist = APIException("Resources not found.", "user.not-exist")


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    async def get_by_ident(self, ident: str) -> Optional[models.UP]:
        with auto_session() as session:
            sentence = select(User).where(or_(User.email == ident, User.username == ident))
            user = session.exec(sentence).first()
            if user is None:
                raise exceptions.UserNotExists()
            return user

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        if len(user_create.username) < 4 or len(user_create.username) > 16:
            next_node = {"message": "length should between: 4~16"}
            raise user_username_illegal.extends(next_node)
        if len(user_create.password) < 6:
            next_node = {"message": "length should above: 6"}
            raise user_password_illegal.extends(next_node)
        if len(user_create.country) != 2 or user_create.country.isalpha() == False:
            raise user_country_illegal

        with auto_session() as session:
            existing_user = session.exec(select(User).where(User.username == user_create.username)).first()
            if existing_user is not None:
                raise exceptions.UserAlreadyExists()
        return await super().create(user_create, safe, request)

    async def authenticate(self, credentials: OAuth2PasswordRequestForm) -> Optional[models.UP]:
        try:
            user = await self.get_by_ident(credentials.username)
        except exceptions.UserNotExists:
            # Run the hasher to mitigate timing attack
            # Inspired from Django: https://code.djangoproject.com/ticket/20760
            self.password_helper.hash(credentials.password)
            return None

        verified, updated_password_hash = self.password_helper.verify_and_update(credentials.password, user.hashed_password)
        if not verified:
            return None
        # Update password hash to a more robust one if needed
        if updated_password_hash is not None:
            await self.user_db.update(user, {"hashed_password": updated_password_hash})

        return user


async def get_user_manager():
    async with async_session() as session:
        yield UserManager(SQLAlchemyUserDatabase(session, User))


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=jwt_secret, lifetime_seconds=60 * 60 * 24 * 30)


def parse_exception(exception: HTTPException) -> APIException:
    if exception.status_code == 500:
        return user_internal
    if exception.status_code == 401:
        return user_unauthorized
    if exception.status_code == 404:
        return user_not_exist
    if exception.status_code == 400:
        if type(exception.detail) == dict:
            if exception.detail["code"] in [
                ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                ErrorCode.REGISTER_INVALID_PASSWORD,
                ErrorCode.RESET_PASSWORD_INVALID_PASSWORD,
            ]:
                next_node = {"message": exception.detail["reason"]}
                return user_password_illegal.extends(next_node)
        if exception.detail == ErrorCode.REGISTER_USER_ALREADY_EXISTS:
            return user_duplicated
        if exception.detail in [
            ErrorCode.LOGIN_BAD_CREDENTIALS,
            ErrorCode.RESET_PASSWORD_BAD_TOKEN,
        ]:
            return user_credentials_incorrect
        if exception.detail == ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS:
            return user_email_duplicated


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

user_router = fastapi_users.get_users_router(User, UserUpdate)
auth_router = fastapi_users.get_auth_router(auth_backend)
register_router = fastapi_users.get_register_router(UserRead, UserWrite)

router.include_router(user_router, prefix="/users", tags=["users"])
router.include_router(auth_router, prefix="/auth/jwt", tags=["auth"])
router.include_router(register_router, prefix="/auth", tags=["auth"])

require_user = fastapi_users.current_user(active=True)
require_user_optional = fastapi_users.current_user(active=True, optional=True)
