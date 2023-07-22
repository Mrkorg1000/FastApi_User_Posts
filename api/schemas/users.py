from pydantic import BaseModel, SecretStr


class UserBase(BaseModel):
    username: str
    email: str


class User(UserBase):
    id: int
    hashed_password: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: SecretStr


class UserOut(UserBase):
    pass