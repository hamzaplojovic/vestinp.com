from pydantic import BaseModel

from fastapi import Body
from fastapi import FastAPI

app = FastAPI()

DATA = []


class Item(BaseModel):
    domain: str
    url: str
    title: str
    short_summary: str
    views: int


class Full(BaseModel):
    items: list[Item]


@app.get('/')
def root():
    return DATA


@app.post('/feed/')
def post_feed(full: Full = Body(...)):
    global DATA
    DATA = full
    return {'status': 200}
