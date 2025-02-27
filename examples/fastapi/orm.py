from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Field, Session, create_engine, select
import uvicorn


class Users(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    password: str = Field(nullable=False)


engine = create_engine("sqlite:///../../examplesDB.db", connect_args={"check_same_thread": False})


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


@asynccontextmanager
async def lifespan(_: FastAPI):
    # executes at startup
    create_db_and_tables()
    yield
    # executes at shutdown


SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI(lifespan=lifespan)


@app.get("/")
def root(session: SessionDep):
    return session.exec(select(Users)).all()


@app.get("/add")
def get_add(name: str, password: str, session: SessionDep):
    user = Users(name=name, password=password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@app.post("/add")
def post_add(user: Users, session: SessionDep):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)