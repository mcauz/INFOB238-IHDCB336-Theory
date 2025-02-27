from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    """
    Base class for all user models.

    Attributes
    ----------
    username : str
        Username of the user.
    password : str
        Password of the user.
    """
    username: str = Field(nullable=False, min_length=1)
    password: str = Field(nullable=False, min_length=1)


class User(UserBase, table=True):
    """
    Models of the User table in the database

    Attributes
    ----------
    id : str | None
        Identifier of the user.
    token : int
        Number of the user tokens.
    auth_token : str | None
        Authentication token of the user.
    """

    __tablename__ = 'User'

    id: int | None = Field(default=None, primary_key=True)
    token: int = Field(default=300, nullable=False)
    auth_token: str | None = Field(default=None)


class UserRegister(UserBase):
    """
    User model for the registration of a new user.

    Attributes
    ----------
    confirm_password : str
        Confirmation of the password for the user.
    """
    confirm_password: str = Field(nullable=False, min_length=1)


class UserLogin(UserBase):
    """
    User model for the connection of a user.
    """
    pass
