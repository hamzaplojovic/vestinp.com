import feedparser


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
            'views': 'separata_function'
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
            'views': 'separata_function'
        }
        content.append(data)
    
    return content


def sandzakhaber_net():
    rss_url = 'https://sandzakhaber.net/feed/'
    parsed_feed = feedparser.parse(rss_url)
    content = []
    for article in parsed_feed.entries:
        data = {
            'url': article['link'],
            'title': article['title'],
            'short_summary': article['summary'],
            # TODO: add adjust for multiple content (index 0,1,2..)
            'description': article['content'][0]['value'],
            'views': 'separata_function'
        }
        content.append(data)
    
    return content


if __name__ == '__main__':
    # t = sandzakpress_net()
    # print(t[0]['description'])
    t = sandzakhaber_net()
    print(t[0]['description'])
