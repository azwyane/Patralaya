from django.urls import path
from feedaggregate.views  import FeedListView
urlpatterns=[

    path('fetch/feed/',FeedListView.as_view(),name='feed_list'),
]