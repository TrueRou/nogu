from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.schemas import UserFull, UserUpdate, UserCreate
from app.users import fastapi_users, auth_backend

app = FastAPI()
scheduler = AsyncIOScheduler()

app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users.get_users_router(UserFull, UserUpdate), prefix="/users", tags=["users"])
app.include_router(fastapi_users.get_register_router(UserFull, UserCreate), prefix="/auth", tags=["auth"])

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)