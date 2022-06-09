from pydantic import BaseModel

from fastapi import Body
from fastapi import FastAPI

app = FastAPI()

DATA = []


class Item(BaseModel):
    url: str
    title: str
    description: str
    short_summary: str
    short_summary: str
    views: str


class Full(BaseModel):
    items: list[Item]


@app.get('/')
def root():
    return {'items': DATA}


@app.post('/feed/')
def post_feed(full: Full = Body(...)):
    global DATA
    DATA = full
    return {'status': 200}
