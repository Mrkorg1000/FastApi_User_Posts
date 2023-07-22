from datetime import timedelta
from typing import Annotated

from core.config import Settings, get_settings
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from schemas.tokens import Token
from schemas.users import User, UserBase
from sqlalchemy.ext.asyncio import AsyncSession

from .dependencies import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    get_db,
)

router = APIRouter(tags=["auth"])


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
    config: Annotated[Settings, Depends(get_settings)],
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config.auth_access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, config=config, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/auth/me/", response_model=UserBase)
async def read_auth_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return User.from_orm(current_user)
