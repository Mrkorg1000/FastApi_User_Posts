from fastapi import FastAPI
from api_ import auth, users, posts, likes, dislikes
from core.database import Base, engine
from core.config import get_settings

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(likes.router)
app.include_router(dislikes.router)


@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        if get_settings().api_debug:
            await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)