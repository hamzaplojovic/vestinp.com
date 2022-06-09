import os

from deta import Deta
from fastapi import Body
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

deta = Deta("a001zjmk_1BZr4RgcEymk9eCkoPQbG4UYtSP2tiry")

db = deta.Base('data')

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.get('/data/')
def root():
    data = db.fetch().items
    if data:
        return data[0]['items']
    return None


@app.post('/feed/')
def post_feed(key: str, full: Full = Body(...)):
    if key == KEY:
        # empty the list
        for x in db.fetch().items:
            db.delete(x['key'])
        return {'status': db.put(jsonable_encoder(full))}
    return {'status': 400}
