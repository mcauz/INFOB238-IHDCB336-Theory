import uvicorn
from typing import Annotated
from fastapi import FastAPI, Depends, WebSocket, Request, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel.ext.asyncio.session import AsyncSession
from contextlib import asynccontextmanager
from server.database import Database
from server.api import create_api
from server.websocket import WebsocketManager
from server.interceptors import create_auth_interceptor

COOKIE_LIFETIME = 3600

# Creates a connection to the database
database = Database("./database.db")
SessionDep = Annotated[AsyncSession, Depends(database.get_db_access)]


# Creates and populates the database tables
@asynccontextmanager
async def lifespan(_: FastAPI):
    # executes at startup
    await database.create_db_and_tables()
    await database.populate_db()
    yield
    # executes at shutdown

# Loads guards
auth_guard = create_auth_interceptor(SessionDep)

# Creates a FastAPI application and mounts the public folder
app = FastAPI(lifespan=lifespan)
app.mount("/api", create_api(SessionDep, auth_guard))
app.mount("/", StaticFiles(directory="public"), name="public")

# Add CORS Policy
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    return FileResponse("public/index.html")


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    websocket_manager = WebsocketManager()
    await websocket_manager.accept(ws)
    await websocket_manager.listening(ws)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
