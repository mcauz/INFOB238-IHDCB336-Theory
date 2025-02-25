from pydantic import BaseModel
from .cartItem import CartItem


class Cart(BaseModel):
    id: int | None = None
    items: list[CartItem]
