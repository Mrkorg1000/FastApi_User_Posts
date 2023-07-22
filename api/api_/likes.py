from typing import Annotated
from crud import likes as crud
from fastapi import APIRouter, Depends
from schemas.likes import Like, LikeCreate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .dependencies.db import get_db
from schemas.users import User
# from db.users import User
from db.posts import Post as DBPost
from .dependencies.auth import get_current_active_user

router = APIRouter(tags=["likes"])


@router.post("/likes", response_model=Like)
async def create_like(like: LikeCreate, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_current_active_user)]):
    user_id = current_user.id

    # post = await db.get(DBPost, like.post_id)
    # if post.user_id == user_id:
        
    db_like = await crud.add_like(db, like, user_id)

    response = Like(id=db_like.id, post_id=db_like.post_id, user_id=db_like.user_id)
    await db.commit()
    return response
