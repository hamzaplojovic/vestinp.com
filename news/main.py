from typing import Union

from fastapi import FastAPI, WebSocket
from feed import sandzakpress_net
from feed import rtvnp_rs
from feed import sandzakhaber_net
from feed import sandzaklive_rs

app = FastAPI()

empty = None

@app.get("/home")
def read_root():
    return {"Hello": "World"}

@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        print(data)
        await websocket.send_text(f"Message text was: {data}")