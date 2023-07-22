from db.posts import Post as DBPost
from db.users import User
from schemas.posts import Post, PostCreate, PostEdit
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
from fastapi import Depends
from api_.dependencies.auth import get_current_active_user


async def get_posts(db: AsyncSession):
    query = select(DBPost)
    result = await db.execute(query)
    return result.scalars().all()


async def add_post(db: AsyncSession, post: PostCreate, user_id: int ) -> DBPost:
    post_kwargs = post.dict()
    post_kwargs['user_id'] = user_id
    db_post = DBPost(**post_kwargs)

    db.add(db_post)
    await db.flush()
    
    await db.refresh(db_post)
    return db_post


async def delete_post(db: AsyncSession, id: int):
    post = await db.get(DBPost, id)
    await db.delete(post)
        
    await db.commit()
    return {"status": True, "message": "The post has been deleted"}


async def edit_post(db: AsyncSession, id: int, new_text: str ):
    
    query = select(DBPost).filter(DBPost.id == id)
    result = await db.execute(query)
    db_post = result.scalar_one_or_none()
    setattr(db_post, 'text', new_text)
    await db.commit()
    await db.refresh(db_post)
    
    return db_post
    