import feedparser
import requests

from bs4 import BeautifulSoup
from requests.api import request


def sandzakpress_net():
    rss_url = 'https://sandzakpress.net/feed/'
    parsed_feed = feedparser.parse(rss_url)

    content = []
    for article in parsed_feed.entries:
        data = {
            'url': article['link'],
            'title': article['title'],
            'short_summary': article['summary'],
            # TODO: add adjust for multiple content (index 0,1,2..)
            'description': article['content'][0],
            'views': sandzakpress_net_views(article['post-id'])
        }
        content.append(data)

    return content


def sandzaklive_rs():
    rss_url = 'https://sandzaklive.rs/feed/'
    parsed_feed = feedparser.parse(rss_url)

    content = []
    for article in parsed_feed.entries:
        data = {
            'url': article['link'],
            'title': article['title'],
            'short_summary': article['summary'],
            # TODO: add adjust for multiple content (index 0,1,2..)
            'description': article['content'][0]['value'],
            'views': sandzalive_rs_views(article['link'])
        }
        content.append(data)

    return content


# def sandzakhaber_net():
#     rss_url = 'https://sandzakhaber.net/feed/'
#     parsed_feed = feedparser.parse(rss_url)
#     content = []
#     for article in parsed_feed.entries:
#         data = {
#             'url': article['link'],
#             'title': article['title'],
#             'short_summary': article['summary'],
#             # TODO: add adjust for multiple content (index 0,1,2..)
#             'description': article['content'][0]['value'],
#             'views': article['post-id']
#         }
#         content.append(data)

#     return content


def rtvnp_rs():
    rss_url = 'https://rtvnp.rs/feed/'
    parsed_feed = feedparser.parse(rss_url)
    content = []
    for article in parsed_feed.entries:
        data = {
            'url': article['link'],
            'title': article['title'],
            'short_summary': article['summary'],
            # TODO: add adjust for multiple content (index 0,1,2..)
            'description': article['content'][0]['value'],
            'views': rtvnp_rs_views(article['link'])
        }
        content.append(data)

    return content

# utils

def sandzakpress_net_views(article_id):
    payload = {
        'action': 'td_ajax_get_views',
        'td_post_ids': f'[{article_id}]'
    }
    r = requests.post('https://sandzakpress.net/wp-admin/admin-ajax.php', data=payload)
    return list(r.json().values())[0]

# def sandzakhaber_net_views(link):
#     r = requests.get(link)
#     parsed_data = BeautifulSoup(r.text, 'lxml')
#     views = parsed_data.find('div', {'class': 'tdb_single_post_views'}).text
#     return views.strip()

def sandzalive_rs_views(link):
    r = requests.get(link)
    parsed_data = BeautifulSoup(r.text, 'lxml')
    views = parsed_data.find('span', {'class': 'meta-views'}).text
    return views.strip().replace(',', '')

def rtvnp_rs_views(link):
    r = requests.get(link)
    parsed_data = BeautifulSoup(r.text, 'lxml')
    views = parsed_data.find('span', {'class': 'total-views'}).text
    return views.split()[0]

if __name__ == '__main__':
    