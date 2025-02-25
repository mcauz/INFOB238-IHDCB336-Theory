from pydantic import BaseModel
from .cart import Cart


class User(BaseModel):
    id: int | None = None
    username: str
    password: str
    token: int
    cart: Cart
    auth_token: str | None = None


class UserRegister(BaseModel):
    username: str
    password: str
    confirm_password: str


class UserLogin(BaseModel):
    username: str
    password: str
