#!/usr/bin/python
import feedparser
import furl
import os
import requests

from datetime import datetime
from deta import Deta

from bs4 import BeautifulSoup
from tqdm import tqdm

deta = Deta(os.environ['DETA_PROJECT_KEY'])

db = deta.Base('items')


def sandzakpress_net():
    rss_url = 'https://sandzakpress.net/feed/'
    parsed_feed = feedparser.parse(rss_url)

    for article in tqdm(parsed_feed.entries):
        article_date = datetime.strptime(article['published'], '%a, %d %b %Y %X %z')
        data = {
            'domain': 'sandzakpress.net',
            'url': article['link'],
            'title': article['title'],
            'short_summary': sandzakpress_net_title_filter(article['summary']),
            # TODO: add adjust for multiple content (index 0,1,2..)
            # 'description': article['content'][0]['value'],
            'views': sandzakpress_net_views(article['post-id']),
            'date': datetime.isoformat(article_date),
            'img': sandzakpress_net_img_finder(article['content'][0]['value'])
        }
        db.put(data, key=data['url'])


def sandzaklive_rs():
    rss_url = 'https://sandzaklive.rs/feed/'
    parsed_feed = feedparser.parse(rss_url)

    for article in tqdm(parsed_feed.entries):
        article_date = datetime.strptime(article['published'], '%a, %d %b %Y %X %z')
        views, img = sandzaklive_rs_views_and_img(article['link'])
        data = {
            'domain': 'sandzaklive.rs',
            'url': article['link'],
            'title': article['title'],
            'short_summary': article['summary'].replace('&#8230;', '..'),
            # TODO: add adjust for multiple content (index 0,1,2..)
            # 'description': article['content'][0]['value'],
            'views': views,
            'date': datetime.isoformat(article_date),
            'img': img

        }
        db.put(data, key=data['url'])


def rtvnp_rs():
    rss_url = 'https://rtvnp.rs/feed/'
    parsed_feed = feedparser.parse(rss_url)
    for article in tqdm(parsed_feed.entries):
        article_date = datetime.strptime(article['published'], '%a, %d %b %Y %X %z')
        views, img = rtvnp_rs_views_and_img(article['link'])
        data = {
            'domain': 'rtvnp.rs',
            'url': article['link'],
            'title': article['title'],
            'short_summary': article['summary'],
            # TODO: add adjust for multiple content (index 0,1,2..)
            # 'description': article['content'][0]['value'],
            'views': views,
            'date': datetime.isoformat(article_date),
            'img': img

        }
        db.put(data, key=data['url'])

# utils


def sandzakpress_net_views(article_id):
    payload = {
        'action': 'td_ajax_get_views',
        'td_post_ids': f'[{article_id}]'
    }
    r = requests.post('https://sandzakpress.net/wp-admin/admin-ajax.php', data=payload)
    return int(list(r.json().values())[0])


def sandzakpress_net_title_filter(text):
    parsed = BeautifulSoup(text, 'lxml')
    return parsed.text.replace('\n', '').split('[…]')[0].strip()


def sandzakpress_net_img_finder(value):
    parsed = BeautifulSoup(value, 'lxml')
    return furl.furl(parsed.img['src']).remove(args=True, fragment=True).url


def sandzaklive_rs_img(value):
    parsed = BeautifulSoup(value, 'lxml')
    return


def sandzaklive_rs_views_and_img(link):
    r = requests.get(link)
    parsed_data = BeautifulSoup(r.text, 'lxml')
    views = parsed_data.find('span', {'class': 'meta-views'}).text
    img = parsed_data.find('figure', {'class': 'single-featured-image'}).img['src']
    return int(views.strip().replace(',', '')), furl.furl(img).remove(args=True, fragment=True).url


def rtvnp_rs_views_and_img(link):
    r = requests.get(link)
    parsed_data = BeautifulSoup(r.text, 'lxml')
    views = parsed_data.find('span', {'class': 'total-views'}).text
    img = parsed_data.find('div', {'class': 'featured-image'}).img['src']
    return int(views.split()[0]),furl.furl(img).remove(args=True, fragment=True).url


sandzakpress_net()
sandzaklive_rs()
rtvnp_rs()
