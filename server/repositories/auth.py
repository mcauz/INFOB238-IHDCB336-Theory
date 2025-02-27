import jwt
import hashlib
from datetime import datetime, timedelta, timezone
from sqlmodel.ext.asyncio.session import AsyncSession
from server.models import User, UserLogin
from server.daos import UserDAO

# to get a string like this run:
# openssl rand -hex 32
AUTH_SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
AUTH_LIFETIME = 3600
AUTH_ALGORITHM = "HS256"


class AuthRepository:
    """
    Repository defining the business operations for the authentication service.
    """
    def __init__(self, db_session: AsyncSession):
        """
        Parameters
        ----------
        db_session: AsyncSession
            Session object to execute request on the database.
        """
        self.__user_dao = UserDAO(db_session)

    def create_authentication_token(self, user_id: int) -> str:
        """
        Creates a new authentication token for the given user.

        Parameters
        ----------
        user_id : int
            Identifier for the user.

        Returns
        -------
        str
            The authentication token.
        """
        to_encode = {"sub": str(user_id), "exp": datetime.now(timezone.utc) + timedelta(seconds=AUTH_LIFETIME)}
        return jwt.encode(to_encode, AUTH_SECRET_KEY, algorithm=AUTH_ALGORITHM)

    async def decode_authentication_token(self, token: str) -> User | None:
        """
        Decodes an authentication token.

        Parameters
        ----------
        token : str
            The authentication token.

        Returns
        -------
        User | None
            The decoded user or None if the token is invalid.
        """
        if token is None:
            return None

        try:
            jwt_payload = jwt.decode(token, AUTH_SECRET_KEY, algorithms=AUTH_ALGORITHM)
            user = await self.__user_dao.read_one(int(jwt_payload["sub"]))
            return user if user is not None and user.auth_token == token else None
        except jwt.ExpiredSignatureError:
            return None

    def hash_password(self, password: str) -> str:
        """
        Gets the hash of a password.

        Parameters
        ----------
        password : str
            The password to hash.

        Returns
        -------
        str
            The hashed password.
        """
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    async def verify_authentication(self, credentials: UserLogin) -> bool:
        """
        Verifies if a user exists with the given username and password.

        Parameters
        ----------
        credentials : UserLogin
            The username and password of the user.

        Returns
        -------
        bool
            True if the user exists, False otherwise.
        """
        user = await self.__user_dao.read_one_by_username(credentials.username)
        hashed_password = self.hash_password(credentials.password)
        return user is not None and hashed_password == user.password
