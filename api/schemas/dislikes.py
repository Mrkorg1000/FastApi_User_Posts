from pydantic import BaseModel


class DislikeBase(BaseModel):
    post_id: int


class DislikeCreate(DislikeBase):
    pass


class Dislike(DislikeBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True