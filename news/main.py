import os

from datetime import datetime
from datetime import timedelta
from deta import Deta
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from itertools import groupby
from operator import itemgetter
from pydantic import BaseModel

KEY = os.environ['KEY']
deta = Deta(os.environ['DETA_KEY'])

db = deta.Base('items')

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
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


@app.get('/data/')
def data():
    data = db.fetch().items
    return data


@app.get('/data/today/top/')
def data_today_top():

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

    last_month = datetime.now() - timedelta(days=30)
    last_month = last_month.isoformat()
    data = db.fetch({'date?gte': f'{last_month}'}).items

    content = []
    for k, v in groupby(data, itemgetter('domain')):
        sorted_data = sorted(v, key=itemgetter('views'), reverse=True)
        content.extend(sorted_data[:2])

    return content
