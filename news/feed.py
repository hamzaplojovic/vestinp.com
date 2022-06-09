import feedparser
import json
import requests

from bs4 import BeautifulSoup
from tqdm import tqdm


def sandzakpress_net():
    rss_url = 'https://sandzakpress.net/feed/'
    parsed_feed = feedparser.parse(rss_url)

    content = []
    for article in tqdm(parsed_feed.entries):
        data = {
            'domain': 'sandzakpress.net',
            'url': article['link'],
            'title': article['title'],
            'short_summary': sandzakpress_net_title_filter(article['summary']),
            # TODO: add adjust for multiple content (index 0,1,2..)
            # 'description': article['content'][0]['value'],
            'views': sandzakpress_net_views(article['post-id'])
        }
        content.append(data)

    return content


def sandzaklive_rs():
    rss_url = 'https://sandzaklive.rs/feed/'
    parsed_feed = feedparser.parse(rss_url)

    content = []
    for article in tqdm(parsed_feed.entries):
        data = {
            'domain': 'sandzaklive.rs',
            'url': article['link'],
            'title': article['title'],
            'short_summary': article['summary'].replace('&#8230;', '..'),
            # TODO: add adjust for multiple content (index 0,1,2..)
            # 'description': article['content'][0]['value'],
            'views': sandzaklive_rs_views(article['link'])
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
    for article in tqdm(parsed_feed.entries):
        data = {
            'domain': 'rtvnp.rs',
            'url': article['link'],
            'title': article['title'],
            'short_summary': article['summary'],
            # TODO: add adjust for multiple content (index 0,1,2..)
            # 'description': article['content'][0]['value'],
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
    return int(list(r.json().values())[0])



def sandzakpress_net_title_filter(text):
    parsed = BeautifulSoup(text, 'lxml')
    return parsed.text.replace('\n', '').split('[…]')[0].strip()    


# def sandzakhaber_net_views(link):
#     r = requests.get(link)
#     parsed_data = BeautifulSoup(r.text, 'lxml')
#     views = parsed_data.find('div', {'class': 'tdb_single_post_views'}).text
#     return int(views.strip())


def sandzaklive_rs_views(link):
    r = requests.get(link)
    parsed_data = BeautifulSoup(r.text, 'lxml')
    views = parsed_data.find('span', {'class': 'meta-views'}).text
    return int(views.strip().replace(',', ''))


def rtvnp_rs_views(link):
    r = requests.get(link)
    parsed_data = BeautifulSoup(r.text, 'lxml')
    views = parsed_data.find('span', {'class': 'total-views'}).text
    return int(views.split()[0])


if __name__ == '__main__':
    data = []
    data_sandzakpress_net = sandzakpress_net()
    data_sandzaklive_rs = sandzaklive_rs()
    data_rtvnp_rs = rtvnp_rs()

    # Pareto's principle 80:20 rule
    data_sandzakpress_net = sorted(data_sandzakpress_net, key=lambda item: item['views'], reverse=True)[:2]
    data_sandzaklive_rs = sorted(data_sandzaklive_rs, key=lambda item: item['views'], reverse=True)[:2]
    data_rtvnp_rs = sorted(data_rtvnp_rs, key=lambda item: item['views'], reverse=True)[:2]

    data.extend(data_sandzakpress_net)
    data.extend(data_sandzaklive_rs)
    data.extend(data_rtvnp_rs)

    requests.post('http://127.0.0.1:8000/feed/', data=json.dumps({"items": data}))
