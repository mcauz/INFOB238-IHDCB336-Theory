from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from contextlib import asynccontextmanager
from server.models import Category, Flower, User
from server.repositories import FlowerRepository, UserRepository, AuthRepository


class Database:
    """
    Manages the connection to the database.
    """

    def __init__(self, path: str):
        """
        Parameters
        ----------
        path : str
            Path to the database file.
        """
        self.__engine = create_async_engine(f"sqlite+aiosqlite:///{path}",connect_args={"check_same_thread": False})

    async def get_db_access(self) -> AsyncSession:
        """
        Gets the session object necessary to access the database.

        Returns
        -------
        AsyncSession
            The session object.
        """
        async_session = sessionmaker(bind=self.__engine, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as session:
            yield session

    async def create_db_and_tables(self):
        """
        Creates the database and tables.
        """
        async with self.__engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def populate_db(self):
        """
        Populates the database.
        """
        # Get access to the database session
        async with asynccontextmanager(self.get_db_access)() as db_session:
            # Check whether flowers exist in the database or not
            flower_repository = FlowerRepository(db_session)
            if len(await flower_repository.get_all()) > 0:
                return

            # Creates categories
            red_category = Category(name='Red flowers')
            orange_category = Category(name='Orange flowers')
            white_category = Category(name='White flowers')

            await flower_repository.create_categories([
                red_category,
                orange_category,
                white_category
            ])

            # Creates flowers
            await flower_repository.create_flowers([
                Flower(name="Gerbera", image="gerbera.jpeg", unit_price=1, quantity=100, category_id=red_category.id),
                Flower(name="Red rose", image="red-rose.jpeg", unit_price=3, quantity=60, category_id=red_category.id),
                Flower(name="Lily", image="lily.jpeg", unit_price=5, quantity=50, category_id=orange_category.id),
                Flower(name="Daisy", image="daisy.jpeg", unit_price=2, quantity=70, category_id=white_category.id),
            ])

            # Creates user
            user_repository = UserRepository(db_session)
            auth_repository = AuthRepository(db_session)
            password = auth_repository.hash_password("Maxime")
            await user_repository.save_user(User(username="Maxime", password=password, token=300))
