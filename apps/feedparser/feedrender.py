import feedparser
import requests

class Render():

    def __init__(self,*args,**kwargs):
        pass

    def fetch(self,uri):
        try:
            response = requests.get(uri).text
        except:
            return None

        return response   

    def parse(self,context):
        if context is None:
            return None
        else:
            feed_parsed = feedparser.parse(context)
            return feed_parsed