from fastapi import FastAPI
from starlette.responses import FileResponse
import uvicorn

app = FastAPI()


@app.get("/firstPage")
def page1():
    return FileResponse('static/firstPage.html')


@app.get("/secondPage")
def page2():
    return FileResponse('static/secondPage.html')

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
