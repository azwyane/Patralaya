import feedparser
import requests

class Render():

    def __init__(self,*args,**kwargs):
        self.uri = kwargs['uri']

    def fetch(self):
        try:
            response = requests.get(self.uri).text
        except:
            return None

        return response   

    def parse(self,context):
        if context is None:
            return None
        else:
            feed_parsed = feedparser.parse(context)
            return feed_parsed