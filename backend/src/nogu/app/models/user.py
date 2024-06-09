import datetime
from enum import IntFlag, auto
from typing import Optional
from fastapi import status
from fastapi_users.schemas import CreateUpdateDictModel
from nogu.app.constants.exceptions import APIException
from nogu.app.database import async_session, manual_session
from sqlmodel import Field, SQLModel, select
from fastapi.security import OAuth2PasswordRequestForm
from nogu.config import jwt_secret

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
from sqlalchemy import or_
from starlette.requests import Request


class UserPriv(IntFlag):
    UNRESTRICTED = auto()
    ADMIN = auto()


class UserBase(SQLModel):
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    country: str = Field(default="XX")


# for fastapi-users to read a user
class UserRead(UserBase):
    id: int
    privileges: UserPriv


# for fastapi-users to create a user
class UserWrite(UserBase, CreateUpdateDictModel):
    password: str


# for fastapi-users to update a user
class UserUpdate(SQLModel):
    password: str | None
    email: str | None
    username: str | None
    country: str | None


class User(UserBase, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    privileges: UserPriv = Field(default=UserPriv.UNRESTRICTED)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    @property
    def is_active(self) -> bool:
        return self.privileges & UserPriv.UNRESTRICTED

    @property
    def is_verified(self) -> bool:
        return True


class UserSrv(IntegerIDMixin, BaseUserManager[User, int]):
    user_username_illegal = APIException("Username illegal.", "user.username.illegal", status_code=status.HTTP_400_BAD_REQUEST)
    user_password_illegal = APIException("Password illegal.", "user.password.illegal", status_code=status.HTTP_400_BAD_REQUEST)
    user_country_illegal = APIException("Country illegal.", "user.country.illegal", status_code=status.HTTP_400_BAD_REQUEST)

    async def get_by_ident(self, ident: str) -> Optional[models.UP]:
        with manual_session() as session:
            sentence = select(User).where(or_(User.email == ident, User.username == ident))
            user = session.exec(sentence).first()
            if user is None:
                raise exceptions.UserNotExists()
            return user

    async def create(self, user_create: schemas.UC, safe: bool = False, request: Optional[Request] = None) -> models.UP:
        if len(user_create.username) < 4 or len(user_create.username) > 16:
            next_node = {"message": "length should between: 4~16"}
            raise UserSrv.user_username_illegal.extends(next_node)
        if len(user_create.password) < 6:
            next_node = {"message": "length should above: 6"}
            raise UserSrv.user_password_illegal.extends(next_node)
        if len(user_create.country) != 2 or user_create.country.isalpha() == False:
            raise UserSrv.user_country_illegal

        with manual_session() as session:
            existing_user = session.exec(select(User).where(User.username == user_create.username)).first()
            if existing_user is not None:
                raise exceptions.UserAlreadyExists()
        return await super().create(user_create, safe, request)

    async def authenticate(self, credentials: OAuth2PasswordRequestForm) -> Optional[models.UP]:
        try:
            user = await self.get_by_ident(credentials.username)
        except exceptions.UserNotExists:
            self.password_helper.hash(credentials.password)
            return None
        verified, updated_password_hash = self.password_helper.verify_and_update(credentials.password, user.hashed_password)
        if not verified:
            return None
        if updated_password_hash is not None:
            await self.user_db.update(user, {"hashed_password": updated_password_hash})
        return user

    async def get_user_manager():
        async with async_session() as session:
            yield UserSrv(SQLAlchemyUserDatabase(session, User))

    def get_jwt_strategy() -> JWTStrategy:
        return JWTStrategy(secret=jwt_secret, lifetime_seconds=60 * 60 * 24 * 30)

    bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
    auth_backend = AuthenticationBackend(name="jwt", transport=bearer_transport, get_strategy=get_jwt_strategy)
    fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

    require_user = fastapi_users.current_user(active=True)
    require_user_optional = fastapi_users.current_user(active=True, optional=True)

    user_router = fastapi_users.get_users_router(User, UserUpdate)
    auth_router = fastapi_users.get_auth_router(auth_backend)
    register_router = fastapi_users.get_register_router(UserRead, UserWrite)
