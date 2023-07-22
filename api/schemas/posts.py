from pydantic import BaseModel
from typing import List, Optional
from .likes import Like
from .dislikes import Dislike


class PostBase(BaseModel):
    text: str


class PostCreate(PostBase):
    pass
    # user_id: int


class PostEdit(PostBase):
    pass


class Post(PostBase):
    id: int
    user_id: int
    likes_count: int
    dislikes_count: int

    

    class Config:
        orm_mode = True