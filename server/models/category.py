from sqlmodel import SQLModel, Field, Relationship
from server.models.flower import Flower


class BaseCategory(SQLModel):
    """
    Base model of a category.

    Attributes
    ----------
    id : str | None
        Identifier of the category.
    name : str
        Name of the category.
    """
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, min_length=1)


class Category(BaseCategory, table=True):
    """
    Model of the Category table in the database.

    Attributes
    ----------
    flowers : list[Flower]
        List of all flowers belonging to the category. This is not a column of the table in the database.
    """

    __tablename__ = 'Category'

    flowers: list["Flower"] = Relationship(
        back_populates="category",
        cascade_delete=True,
        sa_relationship_kwargs={'lazy': 'selectin'}
    )


class CategoryExt(BaseCategory):
    """
    Extension of category model that contains flowers for API response.

    Attributes
    ----------
    flowers : list[Flower]
        List of all flowers belonging to the category.
    """
    flowers: list["Flower"]
