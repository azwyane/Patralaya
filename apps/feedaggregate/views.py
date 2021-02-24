from django.shortcuts import render

from feedaggregate import feedrender
# generic CRUD views in django
from django.views.generic import TemplateView

class FetchFeedMixin():

    def get_rendered_feed(self):
        feed = feedrender.render(self.url)
        return feed

class FeedListView(FetchFeedMixin,TemplateView):
    template_name = "feedaggregate/feed_list.html"
    #temporary url
    url = 'http://arxiv.org/rss/cs?'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        feed_rendered = self.get_rendered_feed()
        context['feed_info'] = feed_rendered.feed
        context['feed_body'] = feed_rendered.entries
        return context