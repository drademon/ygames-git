import time

from fastapi import FastAPI, Depends
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from fastapi.staticfiles import StaticFiles

from auth.local_config import auth_backend, fastapi_users, current_user
from auth.models import User
from auth.schemas import UserRead, UserCreate

from operations.router import router as router_oper
from tasks.router import router as router_tasks
from pages.router import router as router_page
from chat.router import router as router_chat
from redis import asyncio as aioredis

app = FastAPI(title="YG games")

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"


@app.get("/protected-route-g")
def protected_route():
    return f"Hello, goose"


@app.get("/long_red")
@cache(expire=30)
async def index():
    time.sleep(5)
    return "success normaly"


app.include_router(router_oper)
app.include_router(router_tasks)
app.include_router(router_page)
app.include_router(router_chat)


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
