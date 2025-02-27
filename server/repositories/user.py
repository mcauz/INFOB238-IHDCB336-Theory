from sqlmodel.ext.asyncio.session import AsyncSession
from server.models import User, UserRegister
from server.daos import UserDAO
from server.repositories.auth import AuthRepository


class UserRepository:
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
        self.__user_dao = UserDAO(db_session)
        self.__auth_repository = AuthRepository(db_session)

    async def create_user(self, user: UserRegister) -> User:
        """
        Creates and stores a new user from registration information.

        Parameters
        ----------
        user : UserRegister
            Information about the user.

        Returns
        -------
        User
            The created user.
        """
        # Hash the user's password
        user.password = self.__auth_repository.hash_password(user.password)

        # Creates and stores a new user
        user = User.model_validate(user)
        await self.__user_dao.create_one(user)
        return user

    async def get_by_username(self, username: str) -> User | None:
        """
        Gets a user with the given username.

        Parameters
        ----------
        username: str
            The username to search for.

        Returns
        -------
        User | None
            The user with the given username if it exists, or None otherwise.
        """
        return await self.__user_dao.read_one_by_username(username)

    async def save_user(self, user: User):
        """
        Saves the user in the database. The user is updated or created depending on their identifier.

        Parameters
        ----------
        user : User
            The user to save.
        """
        await self.__user_dao.update_or_create_one(user)

    async def verify_registration(self, user: UserRegister) -> bool:
        """
        Verifies if the information for a new user are valid.

        Parameters
        ----------
        user : UserRegister
            Information on the new user.

        Returns
        -------
        bool
            True if the information are valid, False otherwise.
        """
        return user.password == user.confirm_password and (await self.__user_dao.read_one_by_username(user.username)) is None
