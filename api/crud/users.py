from db.users import User as DBUser
from schemas.users import User, UserCreate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user(db: AsyncSession, username: str) -> User:
    query = select(DBUser).filter(DBUser.username == username)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user: UserCreate, hashed_password: str) -> User:
    user_kwargs = user.dict()
    user_kwargs.pop("password")
    user_kwargs["hashed_password"] = hashed_password
    user_kwargs["disabled"] = False
    db_user = DBUser(**user_kwargs)

    async with db.begin():
        db.add(db_user)

    await db.refresh(db_user)
    return db_user