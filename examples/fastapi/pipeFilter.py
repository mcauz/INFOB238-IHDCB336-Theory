from typing import Annotated
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from starlette.responses import FileResponse
from pydantic import BaseModel, Field
import uvicorn

app = FastAPI()


class DataRequest(BaseModel):
    name: str = Field(min_length=1)


@app.get("/", response_class=HTMLResponse)
def get_root():
    return FileResponse('static/pipeFilter.html')


@app.post("/", response_class=HTMLResponse)
def post_root(data: Annotated[DataRequest, Form()]):
    raise Exception("This is an error.")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
