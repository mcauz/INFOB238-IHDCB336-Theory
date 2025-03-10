from pydantic import BaseModel


class CartItem(BaseModel):
    id: int
    number: int
