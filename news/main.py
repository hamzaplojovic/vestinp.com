import os

from ctypes import sizeof

from datetime import datetime
from datetime import timedelta
from deta import Deta
from fastapi import Body
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from itertools import groupby
from operator import itemgetter
from pydantic import BaseModel

KEY = os.environ['KEY']
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


class Item(BaseModel):
    domain: str
    url: str
    title: str
    short_summary: str
    views: int
    date: str


class Full(BaseModel):
    items: list[Item]


@app.get('/data/')
def data():
    data = db.fetch().items
    return data


@app.get('/data/today/top/')
def data_today_top():
    # fetch only from today
    yesterday = datetime.now() - timedelta(days=1)
    yesterday = yesterday.isoformat()
    data = db.fetch({'date?gte': f'{yesterday}'}).items


    content = []
    for k, v in groupby(data, itemgetter('domain')):
        sorted_data = sorted(v, key=itemgetter('views'), reverse=True)
        content.extend(sorted_data[:2])

    return content


@app.get('/data/month/top/')
def data_month_top():
    # fetch only from this month
    last_month = datetime.now() - timedelta(days=30)
    last_month = last_month.isoformat()
    data = db.fetch({'date?gte': f'{last_month}'}).items
 
    content = []
    for k, v in groupby(data, itemgetter('domain')):
        sorted_data = sorted(v, key=itemgetter('views'), reverse=True)
        content.extend(sorted_data[:2])

    return content


# @app.post('/feed/')
# def post_feed(key: str, items: Full = Body(...)):
#     if key == KEY:
#         for item in items.items:
#             db.put(jsonable_encoder(item), key=item.url)
#         return {'status': 200}
#     return {'status': 400}
