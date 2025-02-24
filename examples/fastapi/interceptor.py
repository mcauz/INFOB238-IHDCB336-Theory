from fastapi import FastAPI, Request, Response, Depends
import uvicorn

app = FastAPI()


def modify_request(request: Request, text: str):
    request.state.order = request.state.order + " " + text if hasattr(request.state, "order") else text
    return request


async def modify_response(request: Request, call_next, text: str):
    response = await call_next(request)
    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk
    current = response_body.decode("utf-8").replace("\"", "")
    message = (current + " " + text).encode("utf-8")
    response.headers['Content-Length'] = str(len(message))
    return Response(content=message, status_code=response.status_code, headers=dict(response.headers),
                    media_type=response.media_type)


def guard1(request: Request):
    modify_request(request, "G1,")


@app.middleware("http")
async def middleware1(request: Request, call_next):
    text = "M1,"
    request = modify_request(request, text)
    return await modify_response(request, call_next, text)


@app.middleware("http")
async def middleware2(request: Request, call_next):
    text = "M2,"
    request = modify_request(request, text)
    return await modify_response(request, call_next, text)


def guard2(request: Request):
    modify_request(request, "G2,")


@app.get("/", dependencies=[Depends(guard1), Depends(guard2)])
def get_root(request: Request):
    return "Order: " + request.state.order + " Route,"


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)