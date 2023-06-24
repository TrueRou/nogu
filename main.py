import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.users import fastapi_users, auth_backend
import services
from app.schemas import UserFull, UserUpdate, UserCreate


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


@app.on_event("startup")
async def on_startup():
    await services.create_db_and_tables()


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, port=8000)
