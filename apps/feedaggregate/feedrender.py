import feedparser
import requests


def render(url):
    response = requests.get(url).text
    feed_parsed = feedparser.parse(response)
    if feed_parsed.bozo == 1:
        return None
    return feed_parsed
