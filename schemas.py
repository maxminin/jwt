from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    username: str
    email: str


class TokenData(BaseModel):
    username: str
    email: str


class User(BaseModel):
    username: str
    email: str


class UserInDB(User):
    hashed_password: str

