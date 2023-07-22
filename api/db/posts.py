from core.database import Base
from sqlalchemy import ForeignKey, Integer, Text, select, func
from sqlalchemy.orm import Mapped, mapped_column, MapperProperty, column_property, relationship
from db.likes import Like
from db.dislikes import Dislike

class Post(Base):
    __tablename__ = "posts"
    __allow_unmapped__ = True

    id = mapped_column(Integer, primary_key=True, index=True)
    text = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    likes_count: MapperProperty = column_property(
        select(func.count(Like.id))
        .where(Like.post_id == id)
        .correlate_except(Like)
        .scalar_subquery(),
    )

    dislikes_count: MapperProperty = column_property(
        select(func.count(Dislike.id))
        .where(Dislike.post_id == id)
        .correlate_except(Dislike)
        .scalar_subquery(),
    )

    likes = relationship("Like", back_populates='post')

    dislikes = relationship("Dislike", back_populates='post')