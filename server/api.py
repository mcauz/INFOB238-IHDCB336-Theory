from fastapi import FastAPI, HTTPException, status, Depends, Request, Response
from markupsafe import escape
from server.models import User, UserLogin, UserRegister, CartItem
from server.repositories import AuthRepository, FlowerRepository, UserRepository, CartRepository

COOKIE_LIFETIME = 3600


def create_api(SessionDep, auth_guard):
    api = FastAPI()

    @api.get("/categories")
    async def get_categories(db_session: SessionDep):
        flower_repository = FlowerRepository(db_session)
        return await flower_repository.get_by_categories()

    @api.get("/flower/{flower_id}")
    async def get_flower(db_session: SessionDep, flower_id: int):
        flower_repository = FlowerRepository(db_session)
        flower = await flower_repository.get_one(flower_id)

        if flower is None:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Flower not found.")

        return flower

    @api.get("/flowers")
    async def get_flowers(db_session: SessionDep):
        flower_repository = FlowerRepository(db_session)
        flowers = await flower_repository.get_all()
        return flowers

    @api.get("/user", dependencies=[Depends(auth_guard.unauthorized_auth)])
    async def get_user(request: Request):
        return {"token": request.state.user.token}

    @api.patch("/logout")
    async def logout(db_session: SessionDep, user: User | None = Depends(auth_guard.get_user)):
        # If there is an associated user to the token, we remove the token from their information
        if user is not None:
            user.auth_token = None
            user_repository = UserRepository(db_session)
            await user_repository.save_user(user)

        # We send a success response
        return {"success": True}

    @api.post("/login")
    async def post_login(db_session: SessionDep, body: UserLogin):
        # XSS vulnerability
        body.username = escape(body.username)
        body.password = escape(body.password)

        # Checks credentials
        auth_repository = AuthRepository(db_session)
        if not await auth_repository.verify_authentication(body):
            return {"success": False}

        # We create the authentication token
        user_repository = UserRepository(db_session)
        user = await user_repository.get_by_username(body.username)
        user.auth_token = auth_repository.create_authentication_token(user.id)
        await user_repository.save_user(user)

        # We send response
        return {"success": True, "token": user.auth_token}

    @api.post("/register")
    async def post_register(db_session: SessionDep, body: UserRegister):
        # XSS vulnerability
        body.username = escape(body.username)
        body.password = escape(body.password)

        # Checks validity new user's information and adds the user to the user list in case of success
        user_repository = UserRepository(db_session)
        success = await user_repository.verify_registration(body)

        if success:
            await user_repository.create_user(body)

        # We send response
        return {"success": success}

    @api.post("/cart", dependencies=[Depends(auth_guard.unauthorized_auth)])
    async def post_cart(request: Request, db_session: SessionDep, cart: list[CartItem]):
        user = request.state.user
        cart_repository = CartRepository(db_session)
        success = await cart_repository.apply_cart(user, cart)
        return {"success": success}

    return api
