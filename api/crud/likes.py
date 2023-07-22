from db.likes import Like as DBLike
from schemas.likes import LikeCreate
from sqlalchemy.ext.asyncio import AsyncSession


async def add_like(db: AsyncSession, like: LikeCreate, user_id: int) -> DBLike:
    like_kwargs = like.dict()
    like_kwargs['user_id'] = user_id
    db_like = DBLike(**like_kwargs)

    db.add(db_like)
    await db.flush()
    
    await db.refresh(db_like)
    return db_like