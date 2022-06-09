import os

from fastapi import Body
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

DATA = []

KEY = os.environ['KEY']


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
def post_feed(key: str, full: Full = Body(...)):
    if key==KEY:
        global DATA
        DATA = full
        return {'status': 200}
    return {'status': 400}