from sqlmodel.ext.asyncio.session import AsyncSession
from server.models import User
from server.daos import UserDAO, FlowerDAO


class CartRepository:
    """
    Repository defining the business operations for the cart service.
    """

    def __init__(self, db_session: AsyncSession):
        """
        Parameters
        ----------
        db_session: AsyncSession
            Session object to execute request on the database.
        """
        self.__user_dao = UserDAO(db_session)
        self.__flower_dao = FlowerDAO(db_session)

    async def apply_cart(self, user: User, cart: str) -> bool:
        """
        Removes sold flowers from stock and reduces the number of tokens held by the customer. If the customer does not
        have enough tokens, or if there is not enough flower in stock, the operation is cancelled.

        Parameters
        ----------
        user : User
            The user that buy the cart.
        cart : str
            The cart containing the type and number of flowers to buy.

        Returns
        -------
        bool
            True if the operation succeed. False otherwise.

        Raises
        ------
        str
            Human-readable error message when a flower is unknown.
        """
        # Parses the cart content
        cart_split = cart.split(";")

        # Parses each item, retrieves the flower and check the quantity
        flowers = []
        total = 0
        for item in cart_split:
            flower_id, flower_number = item.split("=")
            flower_number = int(flower_number)
            flower = await self.__flower_dao.read_one(flower_id)
            flowers.append(flower)

            if flower is None:
                raise f"Unknown flower: {flower_id}"

            if flower.quantity < flower_number:
                return False

            flower.quantity -= flower_number
            total += flower_number * flower.unit_price

        # Check the number of user's tokens
        if user.token < total:
            return False
        else:
            user.token -= total

        # Apply the change
        try:
            await self.__flower_dao.update_many(flowers)
            await self.__user_dao.update_one(user)
            return True
        except:
            user.token += total
            return False
