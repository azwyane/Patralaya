from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy,reverse
from .models import Bundle


class PublishedBundleFeed(Feed):
    title = 'MY PUBLISHED BUNDLES ON PATRALAYA'
    link = 'home'
    description = 'Latest published bundles'
    
    def items(self):
        return Bundle.published.all().order_by('-published_on')
        
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return truncatewords(item.context, 60)