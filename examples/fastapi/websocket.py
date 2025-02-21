from fastapi import FastAPI, WebSocket
from starlette.responses import FileResponse
from starlette.websockets import WebSocketDisconnect
import uvicorn

app = FastAPI()


@app.get("/")
def root():
    return FileResponse('static/websocket.html')


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    while True:
        try:
            data = await ws.receive_text()
            print(data)
            await ws.send_text(f"Message text was: {data}")
        except WebSocketDisconnect:
            break


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
