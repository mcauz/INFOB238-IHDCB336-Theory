from pydantic import BaseModel
from .flower import Flower


class CartItem(BaseModel):
    id: int | None = None
    flower: Flower
    number: int
