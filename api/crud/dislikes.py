from db.dislikes import Dislike as DBDislike
from schemas.dislikes import DislikeCreate
from sqlalchemy.ext.asyncio import AsyncSession


async def add_dislike(db: AsyncSession, dislike: DislikeCreate, user_id: int) -> DBDislike:
    dislike_kwargs = dislike.dict()
    dislike_kwargs['user_id'] = user_id
    db_dislike = DBDislike(**dislike_kwargs)

    db.add(db_dislike)
    await db.flush()

    await db.refresh(db_dislike)
    return db_dislike