from typing import Annotated, Optional
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
import uvicorn

app = FastAPI()
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

templates = Jinja2Templates(directory="templates")

data = {
    "name": "Maxime",
    "age": 18,
    "students": ["Alexis", "Maria", "Carmen"]
}


class DataRequest(BaseModel):
    name: str = Field(min_length=1)
    age: Optional[int] = None


@app.get("/", response_class=HTMLResponse)
def get_root(request: Request):
    return templates.TemplateResponse(request=request, name="nameTemplate.html", context=data)


@app.post("/", response_class=HTMLResponse)
def post_root(request: Request, data_req: Annotated[DataRequest, Form()]):
    data["name"] = data_req.name
    return templates.TemplateResponse(request=request, name="nameTemplate.html", context=data)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
