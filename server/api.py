from fastapi import FastAPI, HTTPException, status
from server.repositories import AuthRepository, FlowerRepository


def create_api(SessionDep, TokenType):
    api = FastAPI()

    @api.get("/flower/{flower_id}")
    async def get_flower(db_session: SessionDep, flower_id: int, token: TokenType = None):
        # Retrieves the user's information from their authentication token
        auth_repository = AuthRepository(db_session)
        user = await auth_repository.decode_authentication_token(token)

        if user is None:
            return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You must be authenticated.")

        # Retrieves the flower
        flower_repository = FlowerRepository(db_session)
        flower = await flower_repository.get_one(flower_id)

        if flower is None:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Flower not found.")

        # Returns the quantity of flower
        return flower

    @api.get("/flowers")
    async def get_flowers(db_session: SessionDep, token: TokenType = None):
        # Retrieves the user's information from their authentication token
        auth_repository = AuthRepository(db_session)
        user = await auth_repository.decode_authentication_token(token)

        if user is None:
            return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You must be authenticated.")

        # Retrieves and returns flowers
        flower_repository = FlowerRepository(db_session)
        flowers = await flower_repository.get_all()
        return flowers

    return api
