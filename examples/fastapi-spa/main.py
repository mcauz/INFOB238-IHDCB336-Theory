from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
import uvicorn

app = FastAPI()
app.mount("/public", StaticFiles(directory="public"), name="public")

@app.get("/{full_path:path}")
async def get_not_found(full_path: str):
    return FileResponse('index.html')


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
