from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Field, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
import uvicorn


class Users(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    password: str = Field(nullable=False)


engine = create_async_engine("sqlite+aiosqlite:///../../examplesDB.db", connect_args={"check_same_thread": False})


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


@asynccontextmanager
async def lifespan(_: FastAPI):
    # executes at startup
    await create_db_and_tables()
    yield
    # executes at shutdown

SessionDep = Annotated[AsyncSession, Depends(get_session)]
app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root(session: SessionDep):
    return (await session.exec(select(Users))).all()


@app.get("/add")
async def get_add(name: str, password: str, session: SessionDep):
    user = Users(name=name, password=password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@app.post("/add")
async def post_add(user: Users, session: SessionDep):
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)