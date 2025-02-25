from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, Form, Cookie, Request
from fastapi.responses import HTMLResponse
from starlette.responses import FileResponse
from datetime import datetime, timedelta, timezone
from fastapi.templating import Jinja2Templates
import uvicorn
import jwt

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"


class Auth:
    def __init__(self):
        self.token = ""

    def __call__(self, token: Annotated[str | None, Cookie()] = None):
        if token != self.token:
            raise HTTPException(status_code=401, detail="Authentication token is invalid.")


auth = Auth()


def create_jwt_token(username: str):
    to_encode = {"sub": username, "exp": datetime.now(timezone.utc) + timedelta(minutes=15)}
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")


@app.get("/", response_class=HTMLResponse)
def get_root(request: Request):
    return templates.TemplateResponse(request=request, name="guard.html", context={"token": auth.token})


@app.post("/", response_class=HTMLResponse)
def post_root(request: Request, username: Annotated[str, Form()]):
    auth.token = create_jwt_token(username)
    return templates.TemplateResponse(request=request, name="guard.html", context={"token": auth.token})


@app.get("/auth", response_class=HTMLResponse, dependencies=[Depends(auth)])
def get_auth():
    return FileResponse('static/guardAuth.html')


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
