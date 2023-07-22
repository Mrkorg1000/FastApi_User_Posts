from typing import Annotated, List
from .dependencies.auth import get_current_active_user
from db.users import User

from crud import posts as crud
from fastapi import APIRouter, Depends
from schemas.posts import PostCreate, Post
from sqlalchemy.ext.asyncio import AsyncSession

from .dependencies.db import get_db


router = APIRouter(tags=["posts"])

@router.post("/posts", response_model=Post)
async def create_post(post: PostCreate, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_current_active_user)]):
    user_id = current_user.id
    db_post = await crud.add_post(db, post, user_id)
    
    response = Post(id=db_post.id, text=db_post.text, user_id=db_post.user_id, likes_count=0, dislikes_count=0)
    await db.commit()
    return response


@router.get("/posts", response_model=List[Post])
async def get_posts(db: Annotated[AsyncSession, Depends(get_db)]):
    posts = await crud.get_posts(db)
    return posts


@router.delete("/posts/{id}")
async def delete_post(id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.delete_post(db, id)


@router.patch("/posts/{id}", response_model=Post)
async def update_post(id: int, db: Annotated[AsyncSession, Depends(get_db)], text: str):
    updated_post = await crud.edit_post(db, id, text)
    return updated_post


