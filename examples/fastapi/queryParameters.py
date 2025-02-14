from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

templates = Jinja2Templates(directory="templates")

data = {
    "name": "Maxime",
    "age": 18,
    "students": ["Alexis", "Maria", "Carmen"]
}


@app.get("/", response_class=HTMLResponse)
def get_root(request: Request, name: str = "Maxime", age: int = 18):
    data["name"] = name
    data["age"] = age
    return templates.TemplateResponse(request=request, name="nameTemplate.html", context=data)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
