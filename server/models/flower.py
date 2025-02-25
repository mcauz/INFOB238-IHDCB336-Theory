from pydantic import BaseModel
from .category import Category


class Flower(BaseModel):
    id: int | None = None
    name: str
    image: str
    unit_price: int
    quantity: int
    category: Category
    description: str = "No description."
