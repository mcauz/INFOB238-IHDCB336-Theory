import time
from fastapi import FastAPI, Request, Response
import uvicorn

app = FastAPI()


@app.middleware("http")
async def middleware(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    message = ("Time: " + str(process_time) + " seconds").encode("utf-8")
    response.headers['Content-Length'] = str(len(message))
    return Response(content=message, status_code=response.status_code, headers=dict(response.headers),
                    media_type=response.media_type)


@app.get("/")
def get_root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)