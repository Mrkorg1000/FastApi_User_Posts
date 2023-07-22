from typing import Annotated
from crud import dislikes as crud
from fastapi import APIRouter, Depends
from schemas.dislikes import Dislike, DislikeCreate
from sqlalchemy.ext.asyncio import AsyncSession
from .dependencies.db import get_db
from db.users import User
from .dependencies.auth import get_current_active_user

router = APIRouter(tags=["dislikes"])


@router.post("/dislikes", response_model=Dislike)
async def create_dislike(dislike: DislikeCreate, db: Annotated[AsyncSession, Depends(get_db)], current_user: Annotated[User, Depends(get_current_active_user)]):
    user_id = current_user.id
    db_dislike = await crud.add_dislike(db, dislike, user_id)

    response = Dislike(id=db_dislike.id, post_id=db_dislike.post_id, user_id=db_dislike.user_id)
    await db.commit()
    return response