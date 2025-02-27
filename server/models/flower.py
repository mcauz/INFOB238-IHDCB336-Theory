from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

# This condition is to prevent error in editor due to circular import
if TYPE_CHECKING:
    from server.models.category import Category


class Flower(SQLModel, table=True):
    """
    Models of the Flower table in the database.

    Attributes
    ----------
    id : str | None
        Identifier of the flower.
    name : str
        Name of the flower.
    image : str
        Name and extension of the flower image.
    unit_price : int
        Price for one flower.
    quantity : int
        Number of flowers available.
    description : str
        Description of the flower.
    category_id: int
        Identifier of the category to which the flower belongs.
    category : Category
        Information on the category to which the flower belongs. This is not a column of the table in the database.
    """

    __tablename__ = 'Flower'

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, min_length=1)
    image: str = Field(nullable=False, min_length=1)
    unit_price: int = Field(nullable=False)
    quantity: int = Field(nullable=False)
    description: str = Field(default="No description.")
    category_id: int = Field(foreign_key="Category.id")
    category: "Category" = Relationship(
        back_populates="flowers",
        sa_relationship_kwargs={'lazy': 'joined'}
    )
