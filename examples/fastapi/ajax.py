from fastapi import FastAPI
from starlette.responses import FileResponse
from pydantic import BaseModel
import uvicorn

app = FastAPI()


class dataRequest(BaseModel):
    name: str
    age: int


@app.get("/")
def root():
    return FileResponse('static/ajax.html')


@app.get("/myResource")
def my_resource():
    return {"message": "Hello World"}


@app.post("/myResource")
def post_my_resource(data: dataRequest):
    print(data.name, data.age)
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
