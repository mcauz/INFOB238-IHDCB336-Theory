from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from server.models import User


class UserDAO:
    """
    Database Access Object (DAO) defining the CRUD operations on the database User table.
    """

    def __init__(self, db_session: AsyncSession):
        """
        Parameters
        ----------
        db_session : AsyncSession
            Session object to execute request on the database.
        """
        self.__db_session = db_session

    async def create_many(self, items: list[User]):
        """
        Creates many items in the database table.

        Before the operation, each item identifier is set to None to ensure continuity of identifiers, using the
        “auto_increment” database property. After the operation, each item is refreshed with the identifier
        assigned to it.

        Parameters
        ----------
        items : list[User]
            Information on each new item.
        """
        for item in items:
            item.id = None
            self.__db_session.add(item)

        await self.__db_session.commit()

        for item in items:
            await self.__db_session.refresh(item)

    async def create_one(self, item: User):
        """
        Creates a new item in the database table.

        Before the operation, the item identifier is set to None to ensure continuity of identifiers, using the
        “auto_increment” database property. After the operation, the item is refreshed with the identifier
        assigned to it.

        Parameters
        ----------
        item : User
            Information on the new item.
        """
        item.id = None
        await self.update_or_create_one(item)

    async def read_all(self) -> list[User]:
        """
        Reads all items from the database table.

        Returns
        -------
        list[User]
            List of all items stored in the database table.
        """
        return (await self.__db_session.exec(select(User))).all()

    async def read_many(self, items_id: list[int]) -> list[User]:
        """
        Reads many items from the database table based on their identifiers.

        Parameters
        ----------
        items_id : list[int]
            Identifiers of the items to retrieve.

        Returns
        -------
        list[User]
            The items associated with the specified identifiers.
        """
        return filter(lambda x: x in items_id, await self.read_all())

    async def read_one(self, item_id: int) -> User | None:
        """
        Reads one item from the database table based on the identifier.

        Parameters
        ----------
        item_id : int
            Identifier of the item to retrieve.

        Returns
        -------
        User | None
            The item associated with the specified identifier, or None if the item does not exist.
        """
        return await self.__db_session.get(User, item_id)

    async def update_many(self, items: list[User]):
        """
        Updates many items in the database table based on the identifier.

        Parameters
        ----------
        items : list[User]
            New information on each item to be updated.

        Raises
        ------
        TypeError
            An item identifier is not assigned. Use the 'create' methods instead to create new items.
        """
        if any([item.id is None for item in items]):
            raise TypeError('One or more items have not been created.')

        await self.update_or_create_many(items)

    async def update_one(self, item: User):
        """
        Updates an item in the database table based on the identifier.

        Parameters
        ----------
        item : User
            New information on the item to be updated.

        Raises
        ------
        TypeError
            The item identifier is not assigned. Use the 'create' methods instead to create new items.
        """
        if item.id is None:
            raise TypeError('The item has not been created.')

        await self.update_or_create_one(item)

    async def update_or_create_many(self, items: list[User]):
        """
        Updates or creates many items in the database table. When an item has an identifier it is updated,
        otherwise it is created.

        Parameters
        ----------
        items : list[User]
            New information on each item to be updated or created.
        """
        for item in items:
            self.__db_session.add(item)

        await self.__db_session.commit()

        for item in items:
            await self.__db_session.refresh(item)

    async def update_or_create_one(self, item: User):
        """
        Updates or creates an item in the database table. If the item has an identifier it is updated,
        otherwise it is created.

        Parameters
        ----------
        item : User
            New information on the item to be updated or created.
        """
        self.__db_session.add(item)
        await self.__db_session.commit()
        await self.__db_session.refresh(item)

    async def delete_all(self):
        """
        Deletes all items from the database table.
        """
        items = await self.read_all()
        await self.delete_many(items)

    async def delete_many(self, items: list[int] | list[User]):
        """
        Deletes many items from the database table.

        Parameters
        ----------
        items : list[int] | list[User]
            Identifiers of the items to delete or the items themselves.
        """
        if len(items) == 0:
            return

        if type(items[0]) is int:
            items = await self.read_many(items)

        for item in items:
            await self.__db_session.delete(item)
        await self.__db_session.commit()

    async def delete_one(self, item: int | User):
        """
        Deletes one item from the database table.

        Parameters
        ----------
        item : int | Category
            Identifier of the item to delete or the item itself.
        """
        if type(item) is int:
            item = await self.read_one(item)

        await self.__db_session.delete(item)
        await self.__db_session.commit()

    async def read_many_by_username(self, items_username: list[str]) -> list[User]:
        """
        Reads many items from the database table based on their username.

        Parameters
        ----------
        items_username : str
            Usernames of the items to retrieve.

        Returns
        -------
        list[User]
            The items associated with the specified usernames.
        """
        return filter(lambda x: x.username in items_username, await self.read_all())

    async def read_one_by_username(self, item_username: str) -> User | None:
        """
        Reads one item from the database table based on the username.

        Parameters
        ----------
        item_username : str
            Name of the item to retrieve.

        Returns
        -------
        User | None
            The item associated with the specified username, or None if the item does not exist.
        """
        return (await self.__db_session.exec(select(User).where(User.username == item_username))).first()
