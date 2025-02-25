from typing import Annotated
from fastapi import FastAPI, Request, Form, status, Cookie, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models import UserRegister, UserLogin, Cart, User
from datetime import datetime, timedelta, timezone
import uvicorn
import data
import jwt

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

app = FastAPI()
app.mount("/public", StaticFiles(directory="public"), name="public")

templates = Jinja2Templates(directory="templates")


token_type = Annotated[str | None, Cookie()]


def get_flowers_by_category():
    categories = {}
    for flower in data.flowers:
        if flower.category.name not in categories:
            categories[flower.category.name] = []
        categories[flower.category.name].append(flower)
    return categories


def get_user_by_token(token):
    if token is None:
        return None

    try:
        # Decodes the token to retrieve the payload
        jwt_payload = jwt.decode(token, SECRET_KEY, algorithms="HS256")

        # Checks that the token matches a user
        def compare(user):
            return user.auth_token == token and user.username == jwt_payload["sub"]
        return next(iter([user for user in data.users if compare(user)]), None)

    except jwt.ExpiredSignatureError:
        # Token has expired
        return None


def create_jwt_token(username: str, time: int):
    to_encode = {"sub": username, "exp": datetime.now(timezone.utc) + timedelta(seconds=time)}
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")


@app.get("/", response_class=HTMLResponse)
def get_root(request: Request, token: token_type = None):
    # Retrieves the user's information from their authentication token
    user = get_user_by_token(token)

    # Generates the HTML page
    response = templates.TemplateResponse(request=request, name="pages/home.html", context={
        "is_connected": user is not None,
        "token": user.token if user is not None else 0,
        "categories": get_flowers_by_category(),
    })

    # In case the token is defined but invalid, we remove the cookie
    if token is not None and user is None:
        response.delete_cookie("token")

    return response


@app.get("/login", response_class=RedirectResponse)
def get_login(request: Request, token: token_type = None):
    # Retrieves the user's information from their authentication token
    user = get_user_by_token(token)

    # In case the user is authenticated, we redirect them to the home page
    if user is not None:
        return RedirectResponse("/")

    # Generates the HTML page
    return templates.TemplateResponse(request=request, name="pages/login.html", context={})


@app.post("/login", response_class=RedirectResponse)
def post_login(request: Request, body: Annotated[UserLogin, Form()], token: token_type = None):
    # Retrieves the user's information from their authentication token
    user = get_user_by_token(token)

    # Checks credentials only if the user is not authenticated
    if user is None:
        def compare_user(user1: User):
            return user1.username == body.username and user1.password == body.password
        user = next(iter([u for u in data.users if compare_user(u)]), None)

    # In case the authentication failed and the user is not authenticated
    if user is None:
        return templates.TemplateResponse(request=request, name="pages/login.html", context={"login_error": True})

    # In case the user is authenticated, we redirect them to the home page
    response = RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    user.auth_token = create_jwt_token(user.username, 3600)
    response.set_cookie("token", user.auth_token, max_age=3600)
    return response


@app.post("/register", response_class=HTMLResponse)
def post_register(request: Request, body: Annotated[UserRegister, Form()], token: token_type = None):
    # Retrieves the user's information from their authentication token
    user = get_user_by_token(token)

    # In case the user is authenticated, we redirect them to the home page
    if user is not None:
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

    # Checks validity new user's information and adds the user to the user list in case of success
    success = body.password == body.confirm_password and all(u.username != body.username for u in data.users)
    if success:
        ci = []
        c = Cart(id=len(data.carts), items=ci)
        u = User(id=len(data.users), username=body.username, password=body.password, token=300, cart=c)
        data.cart_items.append(ci)
        data.carts.append(c)
        data.users.append(u)

    # Returns the login page
    return templates.TemplateResponse(request=request, name="pages/login.html", context={
        "register_page": not success,
        "register_succeed": success,
        "register_error": not success
    })


@app.get("/logout", response_class=RedirectResponse)
def get_logout(request: Request):
    response = RedirectResponse("/")
    response.delete_cookie("token")
    return response


@app.get("/market", response_class=RedirectResponse)
def get_market(request: Request, token: token_type = None):
    # Retrieves the user's information from their authentication token
    user = get_user_by_token(token)

    # If the user is not authenticate, we redirect to the home page
    if user is None:
        response = RedirectResponse("/")
        response.delete_cookie("token")
        return response

    # We send the market page
    return templates.TemplateResponse(request=request, name="pages/market.html", context={
        "is_connected": user is not None,
        "token": user.token if user is not None else 0,
        "flowers": data.flowers
    })


@app.get("/cart", response_class=RedirectResponse)
def get_cart(request: Request, token: token_type = None):
    # Retrieves the user's information from their authentication token
    user = get_user_by_token(token)

    # If the user is not authenticate, we redirect to the home page
    if user is None:
        response = RedirectResponse("/")
        response.delete_cookie("token")
        return response

    # We send the market page
    return templates.TemplateResponse(request=request, name="pages/cart.html", context={
        "is_connected": user is not None,
        "token": user.token if user is not None else 0,
    })


@app.post("/cart", response_class=RedirectResponse)
def get_cart(request: Request, cart: Annotated[str, Form()], token: token_type = None):
    # Retrieves the user's information from their authentication token
    user = get_user_by_token(token)

    # If the user is not authenticate, we redirect to the home page
    if user is None:
        response = RedirectResponse("/")
        response.delete_cookie("token")
        return response

    # We check the cart
    success = True
    items = []
    sum = 0
    cart_split = cart.split(";")
    for elt in cart_split:
        s = elt.split("=")
        id = int(s[0])
        number = int(s[1])

        flower = [f for f in data.flowers if f.id == id]

        if len(flower) == 0:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown flower: " + id)

        if flower[0].quantity < number:
            success = False
            break

        items.append((flower[0], number))
        sum += number * flower[0].unit_price

    success = success and user.token >= sum

    # In case of success we buy the flowers
    if success:
        for (flower, number) in items:
            flower.quantity -= number
        user.token -= sum

    # We send the market page
    return templates.TemplateResponse(request=request, name="pages/cart.html", context={
        "is_connected": user is not None,
        "token": user.token if user is not None else 0,
        "success": success,
        "error": not success
    })


@app.get("/{full_path:path}", response_class=HTMLResponse)
def get_not_found(request: Request, full_path: str, token: token_type = None):
    # Retrieves the user's information from their authentication token
    user = get_user_by_token(token)

    # We send the market page
    return templates.TemplateResponse(request=request, name="pages/notFound.html", context={
        "is_connected": user is not None,
        "token": user.token if user is not None else 0,
    })


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
