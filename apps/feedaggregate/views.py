from django.shortcuts import render

from feedaggregate import feedrender
# generic CRUD views in django
from django.views.generic import TemplateView

class FetchFeedMixin():
    uri = None

    def get_uri(self):
        if getattr(self,'uri',None) is None:
            raise 'No feed url given'
        return self.uri

    def get_rendered_feed(self):
        feed = feedrender.Render(uri=self.uri)
        fetch = feed.fetch()
        feed = feed.parse(fetch)
        return feed

class FeedListView(FetchFeedMixin,TemplateView):
    template_name = "feedaggregate/feed_list.html"
    #temporary uri
    uri = 'http://127.0.0.1:8000/bundle/published/all/feed.xml'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        feed_uri = self.get_uri()
        feed_rendered = self.get_rendered_feed()
        context['feed_uri'] = feed_uri
        context['feed_rendered'] = feed_rendered
        return context