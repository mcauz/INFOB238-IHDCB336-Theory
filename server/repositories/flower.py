from sqlmodel.ext.asyncio.session import AsyncSession
from server.models import Category, CategoryExt, Flower
from server.daos import CategoryDAO, FlowerDAO


class FlowerRepository:
    """
    Repository defining the business operations for the flower service.
    """
    def __init__(self, db_session: AsyncSession):
        """
        Parameters
        ----------
        db_session: AsyncSession
            Session object to execute request on the database.
        """
        self.__category_dao = CategoryDAO(db_session)
        self.__flower_dao = FlowerDAO(db_session)

    async def create_categories(self, categories: list[Category]):
        """
        Creates a list of categories.

        Parameters
        ----------
        categories: list[Category]
            Information on the new categories.
        """
        await self.__category_dao.create_many(categories)

    async def create_flowers(self, flowers: list[Flower]):
        """
        Creates a list of flowers.

        Parameters
        ----------
        flowers: list[Flower]
         Information on the new flowers.
        """
        await self.__flower_dao.create_many(flowers)

    async def get_all(self) -> list[Flower]:
        """
        Gets all flowers.

        Returns
        -------
        list[Flower]
            List of all flowers.
        """
        return await self.__flower_dao.read_all()

    async def get_by_categories(self) -> list[CategoryExt]:
        """
        Gets flowers by categories.

        Returns
        -------
        list[CategoryExt]
            List of categories with their property 'flowers'.
        """
        categories = await self.__category_dao.read_all()
        return [CategoryExt.model_validate(category) for category in categories]
