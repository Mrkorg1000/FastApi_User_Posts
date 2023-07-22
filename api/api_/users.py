from typing import Annotated

from crud import users as crud
from fastapi import APIRouter, Depends, HTTPException
from schemas.users import UserCreate, UserOut
from sqlalchemy.ext.asyncio import AsyncSession

from .dependencies.db import get_db
from .dependencies.auth import get_password_hash

router = APIRouter(tags=["users"])


@router.post("/users", response_model=UserOut)
async def create_user(user: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    user = await crud.create_user(
        db, user, get_password_hash(user.password.get_secret_value())
    )
    return UserOut(username=user.username, email=user.email)


@router.get("/users/{username}", response_model=UserOut)
async def read_user(username: str, db: Annotated[AsyncSession, Depends(get_db)]):
    user = await crud.get_user(db, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut(username=user.username, email=user.email)